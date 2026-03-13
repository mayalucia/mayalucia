# [[file:../../codev/01-reproducing-grokking.org::*2.2 Visualizing Learning Curves][2.2 Visualizing Learning Curves:1]]
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from typing import Dict, Any

def plot_learning_curves(history: Dict[str, Any]):
    """
    Plots the training and testing loss and accuracy curves.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Loss Plot
    ax1.plot(history["step"], history["train_loss"], label="Train Loss")
    ax1.plot(history["step"], history["test_loss"], label="Test Loss")
    ax1.set_xlabel("Training Steps")
    ax1.set_ylabel("Loss")
    ax1.set_title("Loss Curves")
    ax1.set_yscale("log")
    ax1.legend()
    ax1.grid(True)

    # Accuracy Plot
    ax2.plot(history["step"], history["train_acc"], label="Train Accuracy")
    ax2.plot(history["step"], history["test_acc"], label="Test Accuracy")
    ax2.set_xlabel("Training Steps")
    ax2.set_ylabel("Accuracy")
    ax2.set_title("Accuracy Curves")
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.savefig("learning_curves.png")
    plt.close()
# 2.2 Visualizing Learning Curves:1 ends here

# [[file:../../codev/01-reproducing-grokking.org::*2.3 Visualizing the Activation Surface][2.3 Visualizing the Activation Surface:1]]
import jax
import jax.numpy as jnp
import numpy as np
import equinox as eqx
from .core import GrokkingTransformer
import matplotlib.pyplot as plt # Already imported, but good practice

def plot_activation_surface(
    model_params: GrokkingTransformer,
    static_model: GrokkingTransformer,
    p: int,
    target_logit: int = 0,
    filename: str = "activation_surface.png"
):
    """
    Renders a 3D surface plot of a specific logit's activation 
    across all possible (a, b) inputs.
    """
    # Reconstitute the full model from the saved parameters and the static structure
    model = eqx.combine(model_params, static_model)

    # 1. Generate the full PxP input grid
    a_range = np.arange(p)
    b_range = np.arange(p)
    a, b = np.meshgrid(a_range, b_range, indexing='ij')
    x_all = jnp.array(np.stack([a.flatten(), b.flatten()], axis=1))

    # 2. Run a forward pass to get logits
    logits = jax.vmap(model)(x_all) # Shape: (P*P, P)

    # 3. Extract the target logit's activation and reshape to grid
    z = logits[:, target_logit].reshape((p, p))

    # 4. Render the 3D surface
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    surf = ax.plot_surface(
        np.array(a), 
        np.array(b), 
        np.array(z), 
        cmap='viridis', 
        edgecolor='none'
    )
    
    ax.set_xlabel('Input a')
    ax.set_ylabel('Input b')
    ax.set_zlabel(f'Logit[{target_logit}] Activation')
    ax.set_title(f'Activation Surface for Target Logit {target_logit}')
    
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
    plt.savefig(filename)
    plt.close()
# 2.3 Visualizing the Activation Surface:1 ends here
