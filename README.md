# Ellery — federal pursuits, handled with care

A responsive marketing site for independent architecture and engineering firms. The current creative direction uses the working name **Ellery**, an original overlapping-leaf symbol, black and mint, Geist and Inter typography, and original botanical and architectural imagery. `brand-directions.html` retains Ellery, Bracken, and Avenell for comparison.

## Preview

```sh
python3 serve.py
```

Run from the repository and open http://localhost:8747. Static HTML/CSS/JavaScript; no application build or runtime packages. The preview supports byte ranges for reliable video seeking. All site assets and fonts are local, with relative paths suitable for a GitHub Pages repository subpath.

## Pages

- `index.html`: positioning, video walkthrough, feature tabs, and FAQs.
- `system.html`: the complete pursuit workflow and human checkpoints.
- `pricing.html`: one-time setup and managed monthly support, without invented prices.
- `contact.html`: a clear, local introduction-preparation form.
- `demo-transcript.html`: accessible text transcript of the walkthrough.
- `brand-directions.html`: the three exploratory naming and identity directions.

## Feature walkthrough

`assets/ellery-demo.mp4` is an 85-second H.264/AAC video at 1440 × 1000, 24 fps. It follows the actual dashboard frontend through the opportunity pipeline, fit assessment, project recommendations, personnel selection, experience matrix, proposal documents, and searchable firm library. It includes a team-alternate interaction and a project search. Native controls, English captions, a transcript, and five chapter shortcuts are available. The video only loads after a visitor chooses to watch it. Escape closes the player and returns focus.

The supplied `alares_testing` frontend ran in an **isolated local fixture environment**, with synthetic API responses. The capture copy received the new brand and a compact pipeline layout; no production dashboard source or backend was changed. The edit combines actual captured interface states and scrolling with reading pauses, a pointer overlay, explanatory subtitles, and synthesized macOS Samantha narration. It is an edited feature walkthrough, not a continuous recording of a live customer deployment. Prepared documents and scores shown are sample fixture records; this recording does not demonstrate backend generation speed or quality.

No customer database, private documents, signatures, credentials, or private dashboard source files are included. The dashboard's main HTML and CSS were checked against the supplied Downloads folder and matched the repository reference.

To reproduce the video from the included captures and narration:

```sh
python3 -m venv .venv
.venv/bin/pip install -r tools/requirements-media.txt
.venv/bin/python tools/render_demo.py
```

`tools/demo-scenes.json` contains narration, timing, and captions. `assets/demo-stills/` contains the captured screen states; `assets/demo-narration.m4a` is the audio source. `assets/brand-sources.md` documents the visual direction and generated imagery.

## Configure inquiries before launch

A real recipient or form endpoint has not been supplied. The form explicitly says it prepares a local request and sends nothing. It validates required fields, then supports copying or saving the introduction.

Set `contactEmail` at the top of `app.js` to an approved recipient to enable a mail-app draft. Visitors still press Send themselves. For automatic delivery, integrate a real form endpoint and only show success after the endpoint accepts the request.

## Checks and release

```sh
node --check app.js
python3 tools/check_site.py
python3 tools/test_preview.py
```

The link checker validates page IDs, local references and anchors, fonts, image labels, captions, and media assets. Browser review covers desktop/mobile layout, feature-tab keyboard navigation, video playback and chapter seeking, Escape/focus restoration, FAQ disclosure, and the introduction form. The video is also decoded end to end with FFmpeg.

The changes stay on `codex/cinematic-rebuild` for review. Main has not been merged or deployed by this task. Naming is a creative working direction, not a claim of trademark or domain availability.
