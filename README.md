# VAGLO — the pursuit platform

A responsive, four-page marketing site for federal architecture and engineering firms. Static HTML, CSS, and JavaScript; no application build or runtime dependencies.

## Preview

```sh
python3 serve.py
```

Open http://localhost:8747. The preview server disables caching. It serves the current directory, so run it from this repository.

## Pages

- `index.html` — positioning, the product film, Discover / Build / Review, fit, and FAQs.
- `system.html` — the workflow, human checkpoints, and product scope.
- `pricing.html` — setup, monthly service, and the discovery process.
- `contact.html` — demo-request preparation with copy and text-download options.

`styles.css` contains the shared responsive design system. `app.js` handles mobile navigation, accessible product tabs, video playback, and request preparation. Fonts are bundled with their SIL Open Font Licenses in `assets/fonts/`; no third-party requests are required to render the site.

## Product film

`assets/vaglo-trailer.mp4` is a 42-second H.264/AAC film, 1280 × 720 at 24 fps, with an original synthesized instrumental score. `assets/hero-loop.mp4` is a short silent ambient preview. Both load only after a visitor asks to play them. The full film includes native playback, volume and fullscreen controls, caption support, and chapter shortcuts. Escape closes the dialog and restores focus.

The dashboard image uses the actual dashboard CSS and pipeline markup patterns from the supplied `alares_testing` project, branded for VAGLO and populated only with synthetic opportunities. It is not a recording of a live customer installation. Proposal and review sequences are illustrative motion graphics and are labeled accordingly. No client database, personnel records, signatures, credentials, or original proposal documents are included.

The dashboard reference was checked against the user-supplied Downloads copy on 2026-09-13; its `index.html` and `dashboard/dashboard.css` matched the repository copy.

To regenerate the main film and poster:

```sh
python3 -m venv .venv
.venv/bin/pip install -r tools/requirements-media.txt
.venv/bin/python tools/render_trailer.py
```

The renderer reads `assets/dashboard.webp` and the bundled fonts. It uses no live services. The media dependencies are only needed to regenerate the film, not to serve or deploy the site.

## Configure demo requests before launch

The original site used the placeholder `hello@vaglo.example`. A real recipient has not been supplied. Until then, the form explicitly prepares a local request that visitors can copy or download; it does not claim delivery.

To enable opening an email draft, set `contactEmail` at the top of `app.js` to the approved recipient address. The visitor still needs to press Send in their mail app. For automatic delivery, replace that mail-draft flow with your chosen form endpoint and show success only after the endpoint accepts the request.

## Deployment

The existing repository uses GitHub Pages from `main`. Review these changes on the feature branch before merging. All paths are relative and work under a GitHub Pages repository subpath. Bump the stylesheet and script query versions when updating a deployed build.

## Checks

```sh
node --check app.js
python3 tools/check_site.py
```

The static checker validates internal files and anchors, unique IDs, local CSS assets, required accessibility labels, video captions, and the absence of placeholder email destinations. Browser QA also covers desktop and mobile layouts, product-tab keyboard navigation, video play/pause and chapters, Escape/focus restoration, FAQ disclosure, and form validation/preparation.
