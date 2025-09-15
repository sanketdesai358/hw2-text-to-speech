import os
import sys
import asyncio
import tempfile
from pathlib import Path

from dotenv import load_dotenv
from openai import AsyncOpenAI

async def stream_and_save(client: AsyncOpenAI, text: str, voice: str, out_dir: Path, idx: int) -> Path:
    """
    Streams TTS audio for a single line and voice to an MP3 file.
    Returns the path to the saved file.
    """
    filename = f"{voice}_sample_{idx+1}.mp3"
    out_path = out_dir / filename

    print(f"[GEN] ({voice}) {text}")

    async with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice=voice,
        input=text,
    ) as stream:
        await stream.stream_to_file(str(out_path))

    if not out_path.exists():
        print(f"[WARN] Expected output not found: {out_path}")
    else:
        print(f"[SAVED] {out_path}")

    return out_path

def play_audio(path: Path):
    """
    Plays the audio file at the given path using the default system player.
    """
    if sys.platform.startswith("win"):
        os.startfile(str(path))
    elif sys.platform == "darwin":
        import subprocess, shutil
        if shutil.which("afplay"):
            subprocess.run(["afplay", str(path)], check=False)
        else:
            print(f"[INFO] Saved audio to: {path} (install 'afplay' or open manually)")
    else:
        import subprocess, shutil
        if shutil.which("mpg123"):
            subprocess.run(["mpg123", str(path)], check=False)
        elif shutil.which("vlc"):
            subprocess.run(["vlc", "--play-and-exit", str(path)], check=False)
        elif shutil.which("aplay"):
            subprocess.run(["aplay", str(path)], check=False)
        else:
            print(f"[INFO] Saved audio to: {path} (open manually to play)")

async def main():
    # Load API key from .env
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not found in .env")

    client = AsyncOpenAI(api_key=api_key)

    # Demo voices and texts
    voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

    # Simulated effects using text cues
    effect_texts = [
        # High emotion, low pitch and speed (simulate with punctuation, pauses, and descriptive cues)
        "[High emotion, low pitch, slow] The Warriors are going to the finals... Can you believe it? This is incredible! Wow...",
        # Low emotion, high pitch and speed (simulate with flat delivery, short sentences, and cues)
        "[Low emotion, high pitch, fast] The Warriors made the finals. It is what it is. Moving on.",
    ]

    # Output directory for audio files
    out_dir = Path("tts_multi_outputs")
    out_dir.mkdir(exist_ok=True)

    print(f"[INFO] Cycling through {len(voices)} voices and {len(effect_texts)} effect texts.")

    for voice in voices:
        print(f"\n=== Voice: {voice} ===")
        for idx, text in enumerate(effect_texts):
            out_path = await stream_and_save(client, text, voice, out_dir, idx)
            # play_audio(out_path)  # Uncomment to play after generation

    print("\n[DONE] Finished generating all samples.")

if __name__ == "__main__":
    asyncio.run(main())
    asyncio.run(main())
