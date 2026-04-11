#!/usr/bin/env python3
# TRIXPHI Bark Generator - Standalone
# phi^2 + 1/phi^2 = 3 | TRINITY

import sys
import os
from pathlib import Path

def generate_bark(style="trap", output="bark_output.wav"):
    """Generate using Bark - FAST!"""
    print(f"=== Bark Generation: {style} ===")

    # Import BarkGenerator from bark module
    import bark
    gen = bark.BarkGenerator(model_size="small", device="cpu")
    gen.load_model()

    prompts = {
        "trap": "[music] 140 BPM dark trap beat with heavy 808 bass, rolling hi-hats",
        "phonk": "[music] Drift phonk with distorted bass, bells, aggressive drums. 140 BPM",
        "drill": "[music] UK drill beat with sliding 808 and dark melody. 140 BPM",
        "lofi": "[music] 85 BPM lo-fi hip-hop chill beat with vinyl crackle and soft piano",
    }

    prompt = prompts.get(style, prompts["trap"])
    audio = gen.generate_music(prompt=prompt, seed=42)
    gen.save(audio, Path(output))

    gen.unload_model()
    print(f"✅ SAVED: {output}")
    return True


def main():
    import argparse

    parser = argparse.ArgumentParser(description="TRIXPHI Bark Generator")
    parser.add_argument("--style", choices=["trap", "phonk", "drill", "lofi"], default="trap")
    parser.add_argument("--output", default="bark_output.wav")

    args = parser.parse_args()

    return 0 if generate_bark(args.style, args.output) else 1


if __name__ == "__main__":
    sys.exit(main())

