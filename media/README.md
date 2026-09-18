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
- 0:10 — Two school-configurable zones: approximately 800 m approach, 150 m arrival.
- 0:24 — Parent selects children and checks in once; presence and rights are checked.
- 0:32 — Release queue; children remain in class until called.
- 0:40 — Classroom call as the car moves forward.
- 0:48 — Staff verify the collector and confirm handoff.
- 0:56 — Pickup record and parent notification.

The zone distances follow sections 4.2 and 4.3.1 of the Driveline product
specification. The initial arrival radius is 150 m, not 100 m. The outer approach
zone prepares the app; it never authorizes check-in or pages the classroom.
The map is illustrative and not to scale. Changing school geometry requires
validation; this video update does not change application configuration.

Voice: ElevenLabs Bella (American English), `eleven_multilingual_v2`. Two new
clips introduce the benefits and zones; the five existing workflow clips are
reused. Narration is aligned to chapter boundaries and normalized for playback.
The API credential stays outside the repository and is never used by the website.

## Regenerate the silent animation

From the website directory:

```sh
python3 tools/render_demo.py
```

Requires Pillow, ffmpeg with libx264, and Arial fonts. The renderer defaults to
macOS fonts; set `DRIVELINE_FONT_DIR` for a directory containing `Arial.ttf` and
`Arial Bold.ttf`. This regenerates the silent animation and poster; it does not
replace the narrated video. Audio generation and alignment outputs are retained
in the engineering workspace under `.local/demo-zones/`.

Published through the website repository's existing GitHub Pages workflow.
The visible description, download link, and written walkthrough remain removed
as requested. Optional captions are available through the video controls.
