# Rhodo — find the opportunities worth pursuing

A responsive marketing site for independent architecture and engineering firms. Rhodo takes its name from rhodonite, Massachusetts’ state gemstone. The original faceted gem symbol and Geist wordmark reflect the idea of finding valuable opportunities among the noise.

The site retains the previous botanical images from the supplied brand reference at the user’s request. The countryside photo, decorative green status dots, and hero caption/down arrow have been removed. See `assets/brand-sources.md` for provenance.

## Preview

```sh
python3 serve.py
```

Open http://localhost:8747. Six static HTML pages, local assets/fonts, no application build or runtime packages. The preview supports byte ranges for video seeking. Relative paths support GitHub Pages repository subpaths.

## Feature walkthrough

`assets/rhodo-demo.mp4` is a 3:32 H.264/AAC walkthrough at 3840 × 2160, 60 fps. It starts with SAM.gov monitoring and AI document analysis, then follows an opportunity through fit assessment, recommended projects, team alternatives, the experience matrix, section generation, documents, and SF330 review. It explains how saved wording and style feedback guide future drafts, and how pursuit decisions help refine opportunity scoring. It also covers projects, personnel, partner firms, uploads, proposals, scoring rules, metrics, help, folders, and roadmap. Lifecycle and Availability are explicitly identified as work in progress. Native controls, English captions, an accessible transcript, and thirteen chapter shortcuts are included. Video loads on demand. Escape closes the player and restores focus.

The actual frontend ran in an isolated local fixture environment with synthetic records and Rhodo branding. This is an edited sequence of native 4K interface captures, smooth scrolling, and a small pointer overlay. It does not represent a continuous customer session or demonstrate backend generation speed. No customer database, private documents, credentials, or private dashboard source is included.

Narration uses Roger (Laid-Back, Casual, Resonant), Eleven v3, Natural stability (0.5), and a conversational script. The approved base take retains its pitch-preserving 1.10× tempo adjustment and fourteen shortened pauses. Two new takes replace the AI-analysis and feedback chapters at natural speed, each with one long pause shortened to 550 ms. The three original MP3s and `narration-production.json` preserve the source and edit decisions. The adaptation explanation describes saved feedback and decision history; it does not claim that every edit automatically retrains a language model. A brief Rhodo end card follows the narration.

```sh
python3 -m venv .venv
.venv/bin/pip install -r tools/requirements-media.txt
.venv/bin/python tools/prepare_narration.py
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

Checks validate local assets/links, unique IDs, captions, and byte-range support. Chromium viewport review covers all six pages at twenty widths from 320 to 2560 pixels, plus landscape video playback, keyboard navigation, feature tabs, FAQs, and the local introduction form. Images keep their native proportions, forms adapt to available space, and mobile player controls remain accessible. The video is decoded with FFmpeg. Changes remain on `codex/cinematic-rebuild`; main is not merged or deployed.
