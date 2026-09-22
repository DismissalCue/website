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

Voice: all seven chapters use the original ElevenLabs Bella (American English),
`hpp4J3VqNfWAUOO0d1Us`, with `eleven_multilingual_v2`. The US distance
chapter was regenerated using the original generation-history settings:
stability 0.65, similarity boost 0.75, style 0.15, speaker boost enabled,
and speed 1.0. Speech is loudness-normalized to −16 LUFS with a −1.5 dBTP
ceiling before mixing. Six other chapters retain their existing recordings.
The replacement starts at 10.2 seconds and fits the existing caption window;
the following chapter still starts at 24 seconds.

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
the six other chapters from the checked-in narrated video, run with your ElevenLabs API key already set in the process environment:

```sh
python3 tools/narrate_us_zones.py
```

This requires `ELEVENLABS_API_KEY`, curl, and ffmpeg. It makes one paid
ElevenLabs generation request using the original voice and settings, checks
that speech fits the caption window, and builds the full output before replacing
the published asset. The key is never placed in command arguments or committed.
Temporary working files belong in ignored `.local/`. Repeated regeneration
re-encodes the retained audio; prefer a clean checkout of the narrated asset
before rebuilding. The original private audio workspace is not required.

API reference: https://elevenlabs.io/docs/api-reference/text-to-speech/convert

Published through the website repository's existing GitHub Pages workflow.
The visible description, download link, and written walkthrough remain removed
as requested. Optional captions are available through the video controls.

## Additional cartoon story — 2026-09-22

`dismissalcue-story.mp4` is a separate 117.53-second, 1280×720, 30fps H.264/AAC
animated explainer. The original walkthrough is retained. Original vector-like
Pillow artwork shows a pickup line, a teacher in rain/cold/sun, coordinated school
roles, approved siblings/physical handoff, per-child weekday clubs and school-wide early dismissal before a holiday weekend, school help, and a district/board call to action. Characters are
fictional. No customer testimony, measured time saving or certification is claimed.
Feature scenes are labeled **Product vision · In development** and the narration
says “we’re building.” It does not advertise a completed or currently deployed product.

The revised film uses Chris, a conversational American voice, at0.9 speed with
stability0.45, similarity0.75 and style0.05. Natural sentences and longer scene pauses
replace the earlier brisk delivery. The script includes exhaust from idling cars
and asks whether better coordination could reduce time beside tailpipes; it does
not claim measured exposure reduction or eliminated emissions. The original
walkthrough retains Bella. Timestamped speech is cached by voice/script/settings
hash, so visual rerenders do not regenerate narration.
Decoded PCM is cut/padded to exact scene sample counts. Narration is normalized to
−16 LUFS with a −1.5 dBTP target; no licensed third-party music/art is included.
Burned captions support muted playback; the separate VTT and `story.html` transcript
provide accessible alternatives. Provider character timing drives the caption cues.

Sources and retained outputs:

- `dismissalcue-story.json`: editable script, scene durations and captions.
- `dismissalcue-story.en.vtt`, `dismissalcue-story-transcript.txt`: text alternatives.
- `dismissalcue-story-poster.jpg`: poster.
- `../tools/render_story.py`: deterministic original animation, no external image assets.
- `../tools/narrate_story.py`: explicit paid narration generation with private cache.

Render without generating voice:

```sh
python3 tools/render_story.py media/dismissalcue-story.json --output .local/story/silent.mp4
```

Set `FFMPEG` if needed and install Pillow. To generate narration for a changed script,
set `ELEVENLABS_API_KEY` securely in the process environment and run
`python3 tools/narrate_story.py`. Never place credentials in command arguments or Git.
The script uses [ElevenLabs timestamped speech](https://elevenlabs.io/docs/api-reference/text-to-speech/convert-with-timestamps).
Mux `.local/story/silent.mp4` with `.local/story/narration.wav` using H.264 stream copy,
AAC160k and `+faststart`. For a visual-only rerender, reuse the audio track from the
retained final video instead of spending generation credits.

Validation: complete decoded-video/audio check, exact timeline/caption bounds,
nine-scene contact-sheet inspection and responsive Chrome checks at390/1280px,
including real video playback, no autoplay, transcript expansion and preservation
of the original video. This is content/browser QA, not school-product acceptance.
