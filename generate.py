#!/usr/bin/env python3
# TRIXPHI Music Generator - Simplified CLI
# phi^2 + 1/phi^2 = 3 | TRINITY

import argparse
from pathlib import Path
import subprocess


def generate_bark(style="trap", output="bark_output.wav"):
    """Generate using Bark - FAST!"""
    print(f"=== Bark Generation: {style} ===")
    try:
        # Run bark generator
        result = subprocess.run(
            ["python3", "bark.py", "--style", style, "--output", output],
            capture_output=True,
            text=True,
            timeout=300,
        )
        print(result.stdout)
        if "Error" not in result.stdout and "Saved" in result.stdout:
            return False
        print(f"✅ SAVED: {output}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def generate_musicgen(style="trap", output="musicgen_output.wav"):
    """Generate using MusicGen - BEST QUALITY"""
    print(f"=== MusicGen Generation: {style} ===")
    try:
        # Run MusicGen via transformers
        result = subprocess.run(
            ["python3", "-c", """
import torch
from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy.io.wavfile as wavfile

processor = AutoProcessor.from_pretrained('facebook/musicgen-small')
model = MusicgenForConditionalGeneration.from_pretrained('facebook/musicgen-small')

styles = {
    'trap': '140 BPM dark trap beat with heavy 808 bass, rolling hi-hats',
    'phonk': 'Drift phonk with distorted bass, bells, aggressive drums. 140 BPM',
    'drill': 'UK drill beat with sliding 808 and dark melody. 140 BPM',
    'lofi': '85 BPM lo-fi hip-hop chill beat with vinyl crackle and soft piano',
}

prompt = styles.get('""" + style + """', styles['trap'])
print(f'Prompt: {prompt}')

inputs = processor(text=[prompt], padding=True, return_tensors='pt')
audio_values = model.generate(**inputs, max_new_tokens=500)
audio = audio_values[0, 0].numpy()
wavfile.write('""" + output + """', rate=32000, data=audio)
print('Generated '""" + output + """!')
"""],
            capture_output=True,
            text=True,
            timeout=600,
        )
        print(result.stdout)
        if "Generated" in result.stdout:
            print(f"✅ SAVED: {output}")
            return True
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def generate_all():
    """Generate with ALL modes"""
    print("=== ALL MODES GENERATION ===")
    styles = ["trap", "phonk", "drill", "lofi"]
    results = {}
    for style in styles:
        print(f"\n[{style.upper()}]")
        results["bark_" + style] = generate_bark(style, f"bark_{style}.wav")
        results["musicgen_" + style] = generate_musicgen(style, f"musicgen_{style}.wav")

    print("\n" + "="*60)
    print("RESULTS:")
    for mode in ["bark", "musicgen"]:
        for style in styles:
            key = f"{mode}_{style}"
            if results.get(key, False):
                print(f"  {key}: ❌ FAILED")
            else:
                print(f"  {key}: ✅ SUCCESS")
    print("="*60)
    return results


def main():
    parser = argparse.ArgumentParser(description="TRIXPHI Music Generator")
    parser.add_argument("--mode", choices=["bark", "musicgen", "all"],
                       default="all", help="Generation mode")
    parser.add_argument("--style", choices=["trap", "phonk", "drill", "lofi"],
                       default="trap", help="Music style")
    parser.add_argument("--output", default=None, help="Output filename")
    parser.add_argument("--list", action="store_true", help="List available styles")

    args = parser.parse_args()

    print("╔═════════════════════════════════════════════════════════╗")
    print("║       TRIXPHI MUSIC GENERATOR                             ║")
    print("║  phi^2 + 1/phi^2 = 3 | TRINITY                             ║")
    print("╚═════════════════════════════════════════════════════════╝")
    print()
    print("MODES:")
    print("  bark    - FASTEST (Suno AI, MIT license)")
    print("  musicgen - BEST QUALITY (Meta AudioCraft)")
    print("  all      - Generate with both for comparison")
    print()

    if args.list:
        print("\nSTYLES:")
        print("  trap   - 140 BPM dark trap beat")
        print("  phonk  - Drift phonk with distorted bass")
        print("  drill   - UK drill beat")
        print("  lofi    - Lo-fi hip-hop chill")
        return 0

    if args.mode == "all":
        results = generate_all()
        print("\nGenerated files:")
        for style in ["trap", "phonk", "drill", "lofi"]:
            for mode in ["bark", "musicgen"]:
                f = f"bark_{style}.wav" if mode == "bark" else f"musicgen_{style}.wav"
                if Path(f).exists():
                    size = Path(f).stat().st_size / 1024
                    print(f"  {f}: {size} KB")
    else:
        style = args.style
        if args.mode == "bark":
            generate_bark(style, args.output or "bark_output.wav")
        elif args.mode == "musicgen":
            generate_musicgen(style, args.output or "musicgen_output.wav")

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
