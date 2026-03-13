# [[file:../../codev/01-reproducing-grokking.org::*Dependencies][Dependencies:1]]
import jax
import jax.numpy as jnp
import equinox as eqx
import optax
import numpy as np
from typing import Callable, Dict, Tuple, Any
# Dependencies:1 ends here

# [[file:../../codev/01-reproducing-grokking.org::*Data Generator: Modular Addition][Data Generator: Modular Addition:1]]
def generate_modular_addition_data(
    p: int,
    train_fraction: float,
    seed: int = 42
) -> Tuple[jnp.ndarray, jnp.ndarray, jnp.ndarray, jnp.ndarray]:
    """
    Generates the complete P^2 dataset for a + b = c (mod P).
    Returns jax arrays: x_train, y_train, x_test, y_test.
    """
    np.random.seed(seed)

    # 1. Generate all a, b pairs (the full PxP manifold)
    a_range = np.arange(p)
    b_range = np.arange(p)
    a, b = np.meshgrid(a_range, b_range, indexing='ij')

    x_all = np.stack([a.flatten(), b.flatten()], axis=1)

    # 2. Calculate the target output c
    y_all = (x_all[:, 0] + x_all[:, 1]) % p

    # 3. Create a randomized train/test split
    num_samples = len(x_all)
    indices = np.random.permutation(num_samples)
    train_size = int(num_samples * train_fraction)

    train_indices = indices[:train_size]
    test_indices = indices[train_size:]

    # 4. Cast to JAX Device Arrays
    x_train = jnp.array(x_all[train_indices])
    y_train = jnp.array(y_all[train_indices])
    x_test = jnp.array(x_all[test_indices])
    y_test = jnp.array(y_all[test_indices])

    return x_train, y_train, x_test, y_test
# Data Generator: Modular Addition:1 ends here

# [[file:../../codev/01-reproducing-grokking.org::*Model Architecture: The 1-Layer Transformer][Model Architecture: The 1-Layer Transformer:1]]
class GrokkingTransformer(eqx.Module):
    embedding: eqx.nn.Embedding
    pos_encoding: jnp.ndarray
    attention: eqx.nn.MultiheadAttention
    mlp: eqx.nn.MLP
    ln1: eqx.nn.LayerNorm
    ln2: eqx.nn.LayerNorm
    unembedding: eqx.nn.Linear

    def __init__(
        self,
        p: int,
        d_model: int,
        num_heads: int,
        d_mlp: int,
        key: jax.random.PRNGKey
    ):
        keys = jax.random.split(key, 5)
        
        self.embedding = eqx.nn.Embedding(p, d_model, key=keys[0])
        # Two positional encodings for the 'a' and 'b' tokens
        self.pos_encoding = jax.random.normal(keys[1], (2, d_model)) * 0.02
        
        self.attention = eqx.nn.MultiheadAttention(
            num_heads=num_heads,
            query_size=d_model,
            key=keys[2]
        )
        
        self.ln1 = eqx.nn.LayerNorm(d_model)
        self.ln2 = eqx.nn.LayerNorm(d_model)
        
        self.mlp = eqx.nn.MLP(
            in_size=d_model,
            out_size=d_model,
            width_size=d_mlp,
            depth=1,
            activation=jax.nn.relu,
            key=keys[3]
        )
        
        self.unembedding = eqx.nn.Linear(d_model, p, key=keys[4])

    def __call__(self, x: jnp.ndarray) -> jnp.ndarray:
        # x is a single sequence of shape (2,) containing [a, b]
        seq_len = x.shape[0]
        
        # 1. Embed and Add Positional Encoding
        x_emb = jax.vmap(self.embedding)(x)  # (2, d_model)
        x_emb = x_emb + self.pos_encoding[:seq_len]
        
        # 2. Attention Layer
        # The query, key, and value are identical (Self-Attention)
        attn_out = self.attention(
            query=jax.vmap(self.ln1)(x_emb),
            key_=jax.vmap(self.ln1)(x_emb),
            value=jax.vmap(self.ln1)(x_emb)
        )
        x_res = x_emb + attn_out
        
        # 3. MLP Layer
        mlp_out = jax.vmap(self.mlp)(jax.vmap(self.ln2)(x_res))
        x_res = x_res + mlp_out
        
        # 4. Unembedding via Mean Pooling
        x_pool = jnp.mean(x_res, axis=0) 
        logits = self.unembedding(x_pool)
        
        return logits
# Model Architecture: The 1-Layer Transformer:1 ends here

# [[file:../../codev/01-reproducing-grokking.org::*Instrumented Trainer][Instrumented Trainer:1]]
@eqx.filter_jit
def compute_loss(model: GrokkingTransformer, x: jnp.ndarray, y: jnp.ndarray) -> Tuple[jnp.ndarray, jnp.ndarray]:
    # x: (batch_size, 2), y: (batch_size,)
    logits = jax.vmap(model)(x)  # (batch_size, p)
    # Using simple cross-entropy
    one_hot_y = jax.nn.one_hot(y, logits.shape[-1])
    loss = optax.softmax_cross_entropy(logits, one_hot_y).mean()
    accuracy = (jnp.argmax(logits, axis=-1) == y).mean()
    return loss, accuracy

@eqx.filter_jit
def make_step(
    model: GrokkingTransformer, 
    opt_state: optax.OptState, 
    x: jnp.ndarray, 
    y: jnp.ndarray, 
    optimizer: optax.GradientTransformation
):
    (loss, acc), grads = eqx.filter_value_and_grad(compute_loss, has_aux=True)(model, x, y)
    updates, opt_state = optimizer.update(grads, opt_state, model)
    model = eqx.apply_updates(model, updates)
    return model, opt_state, loss, acc

def instrumented_training_loop(
    model: GrokkingTransformer,
    optimizer: optax.GradientTransformation,
    x_train: jnp.ndarray,
    y_train: jnp.ndarray,
    x_test: jnp.ndarray,
    y_test: jnp.ndarray,
    total_steps: int,
    log_freq: int = 100
) -> Dict[str, Any]:
    """
    Executes full-batch gradient descent, recording metrics and parameter snapshots.
    Because the dataset is small (e.g. 97^2 = 9409 items), full batch is standard.
    """
    # Initialize optimizer state for the trainable parameters
    opt_state = optimizer.init(eqx.filter(model, eqx.is_inexact_array))
    
    history = {
        "step": [],
        "train_loss": [], "train_acc": [],
        "test_loss": [], "test_acc": [],
        "snapshots": []
    }
    
    for step in range(total_steps):
        model, opt_state, train_loss, train_acc = make_step(
            model, opt_state, x_train, y_train, optimizer
        )
        
        # Save state at specific intervals. In practice, grokking often requires
        # 10^4 to 10^5 steps, so we use logarithmic or semi-logarithmic snapshotting.
        if step % log_freq == 0 or step == total_steps - 1:
            test_loss, test_acc = compute_loss(model, x_test, y_test)
            
            history["step"].append(step)
            history["train_loss"].append(float(train_loss))
            history["train_acc"].append(float(train_acc))
            history["test_loss"].append(float(test_loss))
            history["test_acc"].append(float(test_acc))
            
            # Save the pure pytree of parameters for later analysis
            history["snapshots"].append(
                eqx.filter(model, eqx.is_array))
            
            if step % (log_freq * 10) == 0:
                print(f"Step {step:05d} | Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.4f} | "
                      f"Test Loss: {test_loss:.4f} | Test Acc: {test_acc:.4f}")
                
    return history
# Instrumented Trainer:1 ends here
