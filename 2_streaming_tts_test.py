import os
import sys
import asyncio
import tempfile
from pathlib import Path

from dotenv import load_dotenv
from openai import AsyncOpenAI


async def speak_line(client: AsyncOpenAI, text: str) -> None:
    """
    Streams TTS audio for a single line to a temporary MP3 file, then plays it.
    """
    if not text.strip():
        return

    print(f"\n[SAY] {text}")

    # Temp MP3 file (overwritten for each line)
    out_path = Path(tempfile.gettempdir()) / "openai_tts_line.mp3"

    # Stream server audio -> file (default format is MP3 in this SDK)
    async with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text,
    ) as stream:
        # IMPORTANT: await the coroutine in the async SDK
        await stream.stream_to_file(str(out_path))

    # Safety: ensure the file really exists before trying to play it
    if not out_path.exists():
        print(f"[WARN] Expected output not found: {out_path}")
        return

    # --- Playback ---
    if sys.platform.startswith("win"):
        # Opens with default Windows app (Media Player/Edge)
        os.startfile(str(out_path))
        # Optional: pause a bit so lines don’t overlap if your default player returns immediately
        # import time; time.sleep(2)
    elif sys.platform == "darwin":
        import subprocess, shutil
        if shutil.which("afplay"):
            subprocess.run(["afplay", str(out_path)], check=False)
        else:
            print(f"[INFO] Saved audio to: {out_path} (install 'afplay' or open manually)")
    else:
        import subprocess, shutil
        if shutil.which("mpg123"):
            subprocess.run(["mpg123", str(out_path)], check=False)
        elif shutil.which("vlc"):
            subprocess.run(["vlc", "--play-and-exit", str(out_path)], check=False)
        elif shutil.which("aplay"):
            subprocess.run(["aplay", str(out_path)], check=False)
        else:
            print(f"[INFO] Saved audio to: {out_path} (open manually to play)")


async def main():
    # Load API key from .env
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not found in .env")

    # Init async client
    client = AsyncOpenAI(api_key=api_key)

    # Read narration lines
    txt_path = Path("narration.txt")
    if not txt_path.exists():
        raise FileNotFoundError("narration.txt not found in project folder")

    lines = [ln.strip() for ln in txt_path.read_text(encoding="utf-8").splitlines() if ln.strip()]

    if not lines:
        print("narration.txt is empty—add some lines to narrate.")
        return

    print(f"[INFO] Loaded {len(lines)} line(s) from narration.txt")
    print("[INFO] Starting TTS playback...")

    for i, line in enumerate(lines, 1):
        print(f"[LINE {i}/{len(lines)}]")
        await speak_line(client, line)

    print("\n[DONE] Finished narrating all lines.")


if __name__ == "__main__":
    asyncio.run(main())
