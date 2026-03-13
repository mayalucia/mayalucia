# [[file:../../codev/01-reproducing-grokking.org::*2.1 Main Execution Block][2.1 Main Execution Block:1]]
import jax
import jax.numpy as jnp
import optax
from .core import generate_modular_addition_data, GrokkingTransformer, instrumented_training_loop
from .visualize import plot_learning_curves, plot_activation_surface
import pickle
import equinox as eqx

# --- Hyperparameters ---
P = 97
D_MODEL = 128
NUM_HEADS = 4
D_MLP = 512
TRAIN_FRACTION = 0.4
TOTAL_STEPS = 10000
LOG_FREQ = 100
LEARNING_RATE = 1e-3
WEIGHT_DECAY = 1.0
SEED = 42

def main():
    # --- Setup ---
    key = jax.random.PRNGKey(SEED)
    model_key, data_key = jax.random.split(key)

    x_train, y_train, x_test, y_test = generate_modular_addition_data(
        p=P, train_fraction=TRAIN_FRACTION, seed=SEED
    )

    model = GrokkingTransformer(
        p=P, d_model=D_MODEL, num_heads=NUM_HEADS, d_mlp=D_MLP, key=model_key
    )

    optimizer = optax.adamw(learning_rate=LEARNING_RATE, weight_decay=WEIGHT_DECAY)

    # --- Run Training ---
    print("Starting instrumented training...")
    history = instrumented_training_loop(
        model, optimizer, x_train, y_train, x_test, y_test, TOTAL_STEPS, LOG_FREQ
    )
    print("Training complete.")

    # --- Save and Visualize ---
    print("Saving training history to history.pkl...")
    with open("history.pkl", "wb") as f:
        pickle.dump(history, f)

    print("Generating learning curves plot...")
    plot_learning_curves(history)
    print("Plot saved to learning_curves.png")

    # --- Plot Activation Surface ---
    print("Generating activation surface plot for final model...")
    # We need the static part of the model to recombine with the saved parameters
    static_model = eqx.filter(model, eqx.is_array, inverse=True)
    final_params = history["snapshots"][-1]
    plot_activation_surface(final_params, static_model, P, target_logit=0, filename="activation_surface_final.png")
    print("Plot saved to activation_surface_final.png")

if __name__ == "__main__":
    main()
# 2.1 Main Execution Block:1 ends here
