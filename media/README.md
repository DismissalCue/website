# Simulation demo video

- `driveline-simulation-demo.mp4`: 48-second animated walkthrough, 1280 × 720,
  24 fps, H.264/yuv420p, optimized for progressive web playback.
- `driveline-simulation-poster.jpg`: matching preview image.

The video is silent, with on-screen explanations. It illustrates the planned
product workflow using fictional people and a fictional campus; it is not a
recording of implemented pickup services. No live notifications are sent.

Chapters: approach (0:00), near-school check-in (0:08), release queue (0:16),
classroom call (0:24), staff-confirmed handoff (0:32), pickup record (0:40).

To regenerate from the parent project directory:

```sh
python3 website/tools/render_demo.py
```

Requires Pillow, ffmpeg with libx264, and Arial fonts. The renderer defaults to
macOS system fonts; set `DRIVELINE_FONT_DIR` for another font directory containing
`Arial.ttf` and `Arial Bold.ttf`.

For a future page embed (paths relative to the website root):

```html
<video controls playsinline preload="metadata"
       poster="media/driveline-simulation-poster.jpg"
       style="width:100%;height:auto"
       aria-label="Driveline fictional school pickup simulation with on-screen explanations">
  <source src="media/driveline-simulation-demo.mp4" type="video/mp4">
  <a href="media/driveline-simulation-demo.mp4">Download the simulation video</a>
</video>
```

Created on 2026-09-17. Embedded in the homepage Watch Demo section with native
playback controls. The visible description, download link, and written walkthrough
were removed at the user’s request; ElevenLabs narration is pending access. Published
through the website repository’s existing GitHub Pages workflow.
