# Simulation demo video

- `driveline-simulation-narrated.mp4`: published 64-second demo, 1280 × 720,
  24 fps H.264, AAC voiceover, optimized for progressive web playback.
- `driveline-simulation-demo.mp4`: matching animation without audio.
- `driveline-simulation-poster.jpg`: matching two-zone preview.
- `driveline-narration.en.vtt`: optional English captions in the native player.

The demo illustrates the planned workflow with fictional people and a fictional
campus. It is not evidence of implemented mobile geofencing or measured outcomes.
No live pickup notifications are sent. The opening describes intended benefits;
no unverified performance statistics or universal guarantees are included.

## Chapters

- 0:00 — School pickup challenges and intended benefits.
- 0:10 — Two school-configurable zones: approximately half a mile approach,
  500 feet arrival, with matching US English narration and captions.
- 0:24 — Parent selects children and checks in once; presence and rights are checked.
- 0:32 — Release queue; children remain in class until called.
- 0:40 — Classroom call as the car moves forward.
- 0:48 — Staff verify the collector and confirm handoff.
- 0:56 — Pickup record and parent notification.

The displayed US units are rounded equivalents of the product specification's
800-meter approach and 150-meter arrival examples (sections 4.2 and 4.3.1).
They are presentation values, not new geofence thresholds. The outer approach
zone prepares the app; it never authorizes check-in or pages the classroom.
The map is illustrative and not to scale. Changing school geometry requires
validation; this video update does not change application configuration.

Voice: the opening and five workflow chapters retain the existing ElevenLabs
Bella (American English), `eleven_multilingual_v2`, recording. The US distance
chapter uses macOS Samantha (American English), generated locally at 145 words
per minute because the original voice generation workspace was unavailable.
This chapter has a different voice; no paid service or credential is used for
this update. The replacement starts at 10.2 seconds and fits the existing caption
window; the following chapter still starts at 24 seconds.

## Regenerate the silent animation

From the website directory:

```sh
python3 tools/render_demo.py
```

Requires Pillow, ffmpeg with libx264, and Arial fonts. Set `FFMPEG` to the ffmpeg
executable if it is not on PATH. The renderer defaults to
macOS fonts; set `DRIVELINE_FONT_DIR` for a directory containing `Arial.ttf` and
`Arial Bold.ttf`. This regenerates the silent animation and poster; it does not
replace the narrated video. To replace the distance narration while retaining
the six other chapters from the checked-in narrated video, run on macOS:

```sh
python3 tools/narrate_us_zones.py
```

This requires the locally installed Samantha voice (`say -v Samantha`). It
checks that speech fits the caption window and builds the full output before
replacing the published asset. Temporary working files belong in ignored
`.local/`. Repeated regeneration re-encodes the retained audio; prefer a clean
checkout of the narrated asset before rebuilding. The original private audio
workspace is not required.

Published through the website repository's existing GitHub Pages workflow.
The visible description, download link, and written walkthrough remain removed
as requested. Optional captions are available through the video controls.
