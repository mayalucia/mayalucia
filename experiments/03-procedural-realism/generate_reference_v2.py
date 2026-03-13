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
Reference generation v2: prompts designed to match the SRTM-driven
cross-sectional composition, not a generic "Himalayan valley" shot.

The v2 procedural image shows:
  - Cross-section view: looking across the gorge, not along it
  - Steep dark wall on the left (ENE / Kohistan arc), deep shadow
  - Gentler sunlit wall on the right (WSW / Indian plate), golden dawn light
  - Narrow gorge with the Indus far below at the bottom
  - Snow-capped ridges visible behind the gorge walls
  - Rocky foreground terrace (viewer's position)
  - Strong asymmetry: left wall much taller than right
"""

from pathlib import Path
import torch
from diffusers import StableDiffusionPipeline

OUT = Path(__file__).parent / "references"
OUT.mkdir(exist_ok=True)

MODEL_ID = "stable-diffusion-v1-5/stable-diffusion-v1-5"

# ── Prompts describing the cross-sectional view ──────────────────────

# ── Prompt A: gorge-top cross-section (v2 original) ──
PROMPT_GORGE = (
    "Deep Himalayan gorge cross-section, looking across the valley "
    "steep dark cliff face on the left in deep shadow, "
    "gentler sunlit mountain slope on the right catching golden light, "
    "narrow turquoise river far below at the gorge bottom, "
    "barren terrain with rock faces, "
    "snowy peaks visible behind the gorge walls, "
    "realistic landscape photo golden hour, "
)

# ── Prompt B: river-level, looking up at the walls ──
PROMPT_RIVER = (
    "turquoise glacial river in foreground flowing through deep narrow gorge, "
    "towering dark rock walls on both sides, left wall in deep shadow, "
    "right wall catching golden dawn light, barren rocky terrain, "
    "looking up from river bank, snowy peaks above gorge rim, "
    "landscape photo golden hour"
)

NEGATIVE = (
    "cartoon, illustration, flat colors, vector art, "
    "diagram, schematic, low quality, blurry, "
    "anime, 3d render, text, watermark, painting, "
    "green lush vegetation, forest, tropical"
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

    prompts = [
        ("cross-section", PROMPT_GORGE),
        ("river-level", PROMPT_RIVER),
    ]
    seeds = [42, 137, 271, 404, 512, 777]

    for label, prompt in prompts:
        print(f"\n── {label} ──")
        for seed in seeds:
            print(f"Generating {label} seed={seed}...")
            generator = torch.Generator(device=device).manual_seed(seed)
            image = pipe(
                prompt=prompt,
                negative_prompt=NEGATIVE,
                num_inference_steps=30,
                guidance_scale=7.5,
                width=768,
                height=512,
                generator=generator,
            ).images[0]

            out_path = OUT / f"{label}-seed{seed}.png"
            image.save(out_path)
            print(f"  → {out_path}")

    print(f"\nDone. {len(prompts) * len(seeds)} references in {OUT}")


if __name__ == "__main__":
    main()
