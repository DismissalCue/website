"""Replace only the zones chapter using macOS's local US English voice.

Run after render_demo.py. Existing narration is retained outside 10–24 seconds.
Set FFMPEG to an ffmpeg executable if it is not on PATH. No network/API key needed.
"""
from pathlib import Path
import os
import subprocess
import tempfile
import wave

ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / "media"
FFMPEG = os.environ.get("FFMPEG", "ffmpeg")
NARRATION = (
    "Around half a mile, the approach zone prepares the app. "
    "Near five hundred feet, arrival checks verify presence and pickup rights. "
    "Schools configure these distances for their campus."
)


def main():
    target = MEDIA / "driveline-simulation-narrated.mp4"
    with tempfile.TemporaryDirectory(prefix="driveline-us-") as temp:
        temp = Path(temp)
        voice = temp / "zones.aiff"
        pcm = temp / "zones.wav"
        output = temp / "narrated.mp4"
        subprocess.run(["say", "-v", "Samantha", "-r", "145", "-o", str(voice), NARRATION], check=True)
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", str(voice),
                        "-c:a", "pcm_s16le", str(pcm)], check=True)
        with wave.open(str(pcm)) as sound:
            duration = sound.getnframes() / sound.getframerate()
        if duration > 12.904:
            raise RuntimeError("Voice exceeds the caption window; adjust pacing before publishing")
        # Preserve six original chapters. Replace the complete metric chapter,
        # leaving a 200 ms lead-in and silence until the next chapter at 24 s.
        filters = (
            "[1:a]atrim=start=0:end=10,asetpts=PTS-STARTPTS,aresample=48000[before];"
            "[2:a]aresample=48000,adelay=200,apad,atrim=duration=14[zones];"
            "[1:a]atrim=start=24:end=64,asetpts=PTS-STARTPTS,aresample=48000[after];"
            "[before][zones][after]concat=n=3:v=0:a=1[a]"
        )
        subprocess.run([
            FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(MEDIA / "driveline-simulation-demo.mp4"),
            "-i", str(target), "-i", str(pcm),
            "-filter_complex", filters, "-map", "0:v:0", "-map", "[a]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
            "-t", "64", "-movflags", "+faststart", str(output),
        ], check=True)
        # Replace only once ffmpeg completes successfully.
        target.write_bytes(output.read_bytes())
    print(target)


if __name__ == "__main__":
    main()
