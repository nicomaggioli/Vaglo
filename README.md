# Rhodo — find the opportunities worth pursuing

A responsive marketing site for independent architecture and engineering firms. Rhodo takes its name from rhodonite, Massachusetts’ state gemstone. The original faceted gem symbol and Geist wordmark reflect the idea of finding valuable opportunities among the noise.

The site retains the previous botanical images from the supplied brand reference at the user’s request. The countryside photo, decorative green status dots, and hero caption/down arrow have been removed. See `assets/brand-sources.md` for provenance.

## Preview

```sh
python3 serve.py
```

Open http://localhost:8747. Six static HTML pages, local assets/fonts, no application build or runtime packages. The preview supports byte ranges for video seeking. Relative paths support GitHub Pages repository subpaths.

## Feature walkthrough

`assets/rhodo-demo.mp4` is a 48-second H.264/AAC walkthrough at 3840 × 2160, 60 fps. It follows the supplied dashboard frontend through pipeline, fit assessment, project recommendations, team alternatives, experience matrix, documents, SF330 review, and searchable firm records. Native controls, English captions, an accessible transcript, and five chapter shortcuts are included. Video loads on demand. Escape closes the player and restores focus.

The actual frontend ran in an isolated local fixture environment with synthetic records and Rhodo branding. This is an edited sequence of native 4K interface captures, smooth scrolling, and a small pointer overlay. It does not represent a continuous customer session or demonstrate backend generation speed. No customer database, private documents, credentials, or private dashboard source is included.

Narration uses Roger (Laid-Back, Casual, Resonant), Eleven v3, Natural stability (0.5), and a conversational script. Six long pauses were shortened to 450 ms without changing speech speed or pitch in editing. The original MP3 and `narration-production.json` preserve the source and edit decisions. A brief Rhodo end card follows the narration.

```sh
python3 -m venv .venv
.venv/bin/pip install -r tools/requirements-media.txt
.venv/bin/python tools/render_demo.py
```

`tools/demo-scenes.json` contains the transcript and timings. `assets/demo-stills/` contains lossless 4K captures; `assets/demo-narration-elevenlabs.wav` contains the voice track.

## Inquiries

The contact form prepares a local introduction that visitors can copy or save. It clearly states that nothing is sent. Set `contactEmail` in `app.js` to an approved recipient to enable an email draft, or integrate a real form endpoint before enabling automatic delivery.

## Checks and release

```sh
node --check app.js
python3 tools/check_site.py
python3 tools/test_preview.py
```

Checks validate local assets/links, unique IDs, captions, and byte-range support. Browser review covers desktop/mobile layout, video playback/seeking, navigation, and the contact layout. The video is decoded with FFmpeg. Changes remain on `codex/cinematic-rebuild`; main is not merged or deployed.
