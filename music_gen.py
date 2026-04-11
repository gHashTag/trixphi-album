#!/usr/bin/env python3
# TRIXPHI Music Generator - Simple CLI
# phi^2 + 1/phi^2 = 3 | TRINITY

import sys
import os
from pathlib import Path

# Path adjustments for standalone execution
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

def generate_bark(style="trap", output="bark_output.wav"):
    """Generate using Bark (Suno AI) - FAST!"""
    print(f"=== Bark Generation: {style} ===")
    try:
        from bark import BarkGenerator
        gen = BarkGenerator(model_size="small", device="cpu")
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
        print(f"✅ Saved: {output}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def generate_musicgen(style="trap", output="musicgen_output.wav"):
    """Generate using MusicGen (Meta) - BEST QUALITY"""
    print(f"=== MusicGen Generation: {style} ===")
    try:
        from transformers import AutoProcessor, MusicgenForConditionalGeneration
        import scipy.io.wavfile as wavfile
        import torch

        processor = AutoProcessor.from_pretrained('facebook/musicgen-small')
        model = MusicgenForConditionalGeneration.from_pretrained('facebook/musicgen-small')

        prompts = {
            "trap": "140 BPM dark trap beat with heavy 808 bass, rolling hi-hats",
            "phonk": "Drift phonk with distorted bass, bells, aggressive drums, 140 BPM",
            "drill": "UK drill beat with sliding 808 and dark melody, 140 BPM",
            "lofi": "85 BPM lo-fi hip-hop chill beat with vinyl crackle and soft piano",
        }

        prompt = prompts.get(style, prompts["trap"])
        print(f"Prompt: {prompt}")
        print("Generating... (30-60 seconds)")

        inputs = processor(text=[prompt], padding=True, return_tensors='pt')
        audio_values = model.generate(**inputs, max_new_tokens=500)
        audio = audio_values[0, 0].numpy()

        wavfile.write(output, rate=32000, data=audio)
        print(f"✅ Saved: {output}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def generate_lightweight(style="trap", output="lightweight_output.wav"):
    """Generate using NumPy - FASTEST (no ML)"""
    print(f"=== Lightweight Generation: {style} ===")
    try:
        from generative import ProceduralGenerator
        from effects import SimpleEffects
        from mixer import SimpleMixer

        gen = ProceduralGenerator(sample_rate=48000, seed=42)
        fx = SimpleEffects(sample_rate=48000)
        mixer = SimpleMixer(sample_rate=48000)

        bpm = 140
        beat = gen.generate_beat(30, bpm, "trap")
        bass = gen.generate_bassline(30, bpm, "trap")

        mix = mixer.mix(beat, bass, vocal_level_db=-10)
        mix = mixer.master(mix, target_lufs=-14)

        gen.save(mix, Path(output))
        print(f"✅ Saved: {output}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    import argparse

    parser = argparse.ArgumentParser(description="TRIXPHI Music Generator")
    parser.add_argument("--mode", choices=["bark", "musicgen", "lightweight", "all"],
                       default="all", help="Generation mode")
    parser.add_argument("--style", choices=["trap", "phonk", "drill", "lofi"],
                       default="trap", help="Music style")
    parser.add_argument("--output", default=None, help="Output file prefix")

    args = parser.parse_args()

    print("╔═════════════════════════════════════════════════════════╗")
    print("║         TRIXPHI MUSIC GENERATOR                             ║")
    print("║  phi^2 + 1/phi^2 = 3 | TRINITY                             ║")
    print("╚═════════════════════════════════════════════════════════╝")
    print()

    prefix = args.output or "trixphi"

    if args.mode == "all":
        for mode in ["lightweight", "bark", "musicgen"]:
            output = f"{prefix}_{mode}.wav"
            if mode == "lightweight":
                generate_lightweight(args.style, output)
            elif mode == "bark":
                generate_bark(args.style, output)
            elif mode == "musicgen":
                generate_musicgen(args.style, output)
    else:
        output = f"{prefix}_{args.mode}.wav"
        if args.mode == "lightweight":
            generate_lightweight(args.style, output)
        elif args.mode == "bark":
            generate_bark(args.style, output)
        elif args.mode == "musicgen":
            generate_musicgen(args.style, output)

    print()
    print("╔═════════════════════════════════════════════════════════╗")
    print("║                    COMPLETE                               ║")
    print("╚═══════════════════════════════════════════════════════╝")

    # Try to open generated files
    try:
        import subprocess
        if args.mode == "all":
            for mode in ["lightweight", "bark", "musicgen"]:
                f = Path(f"{prefix}_{mode}.wav")
                if f.exists():
                    subprocess.run(["open", str(f.absolute())], check=False)
        else:
            f = Path(f"{prefix}_{args.mode}.wav")
            if f.exists():
                subprocess.run(["open", str(f.absolute())], check=False)
    except:
        pass


if __name__ == "__main__":
    main()
