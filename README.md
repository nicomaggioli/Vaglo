# VAGLO — marketing site

Static site. No build step, no dependencies, no framework.

```
index.html      The pitch
pricing.html    How pricing works
system.html     The full walkthrough
contact.html    Discovery-call request form
styles.css      Design tokens and all styling
app.js          Nav, scroll reveal, demo dashboard, form handling, chat assistant
assets/         Logo, favicon, photography
```

## Running it locally

```bash
python3 serve.py
```

Then open http://localhost:8747.

Use `serve.py` rather than `python3 -m http.server`. The built-in server sends no cache
headers at all, so browsers apply their own guess and will happily hand you a stale
`index.html` for hours while you wonder why an edit did not take. `serve.py` is the same
thing with `Cache-Control: no-store` on every response.

Opening the files directly over `file://` mostly works, but some browsers block the fonts.

## Deploying

Pushes to `main` deploy automatically to GitHub Pages. Any other static host works too —
there is no server and no database.

Asset links carry a `?v=` query string for cache busting. Bump it when you change CSS or JS,
or returning visitors will be served the old file.

## Design notes

One typeface, Schibsted Grotesk, weights 400–700, loaded from Google Fonts. That is the only
external request the pages make.

Every colour is a token in the `:root` block at the top of `styles.css`. Edit that block and
nothing else to reskin the entire site.

The demo dashboard on the homepage is driven by a single CSS variable, `--b` — the same
mechanism the real product uses to theme itself per firm. It carries placeholder data only:
no real firm, person, project or contract appears anywhere in it, and it must stay that way.
