# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = [
#   "torch>=2.1",
#   "diffusers>=0.25",
#   "transformers>=4.36",
#   "accelerate>=0.25",
#   "safetensors",
# ]
# ///
"""
Experiment 03 — Procedural Realism
Step 1: Generate reference images using Stable Diffusion locally (MPS).

First pass: one panel — the Indus gorge at dawn, viewed from
the Thalpan petroglyph terrace toward Nanga Parbat.
"""

from pathlib import Path
import torch
from diffusers import StableDiffusionPipeline

OUT = Path(__file__).parent / "references"
OUT.mkdir(exist_ok=True)

MODEL_ID = "stable-diffusion-v1-5/stable-diffusion-v1-5"

# ── Prompts ──────────────────────────────────────────────────────────
# Descriptive, grounded in the real geography.
# Negative prompt suppresses the cartoon quality we're escaping.

PROMPT = (
    "Indus river gorge at dawn, view from a rocky terrace toward "
    "Nanga Parbat summit with alpenglow, deep narrow valley, "
    "dark gneiss rock walls, turquoise glacial river below, "
    "sparse juniper on dry slopes, clear Himalayan sky, "
    "Karakoram Highway visible on far bank, "
    "realistic landscape photography, golden hour light, "
    "high detail, atmospheric perspective"
)

NEGATIVE = (
    "cartoon, illustration, flat colors, vector art, "
    "diagram, schematic, low quality, blurry, "
    "anime, 3d render, text, watermark"
)

# ── Generate ─────────────────────────────────────────────────────────

def main():
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"Device: {device}")

    print(f"Loading model: {MODEL_ID}")
    pipe = StableDiffusionPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.float16 if device == "mps" else torch.float32,
        safety_checker=None,
    )
    pipe = pipe.to(device)

    # Generate a few seeds so we can pick the best reference
    seeds = [42, 137, 271, 404]
    for seed in seeds:
        print(f"Generating seed={seed}...")
        generator = torch.Generator(device=device).manual_seed(seed)
        image = pipe(
            prompt=PROMPT,
            negative_prompt=NEGATIVE,
            num_inference_steps=30,
            guidance_scale=7.5,
            width=768,
            height=512,
            generator=generator,
        ).images[0]

        out_path = OUT / f"gorge-dawn-seed{seed}.png"
        image.save(out_path)
        print(f"  → {out_path}")

    print(f"\nDone. {len(seeds)} references in {OUT}")


if __name__ == "__main__":
    main()
