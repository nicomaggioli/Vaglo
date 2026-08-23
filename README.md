# VAGLO — marketing site

Static site. No build step, no dependencies, no framework. Three pages plus a stylesheet
and one script.

```
index.html      The main pitch
system.html     The deep technical tour (honest constraints included)
contact.html    Discovery-call request form
styles.css      Design tokens + all styling
app.js          Brand repainter, sticky nav, scroll reveal, form handling
assets/mark.svg Favicon
```

---

## Before you put this live — do these five things

**1. Verify the name.** Check `VAGLO` for trademark conflicts in Class 42 (software) and
Class 35 (business services) at [tmsearch.uspto.gov](https://tmsearch.uspto.gov), and check
domain availability yourself. The name came out of a scored panel, not a legal clearance.

**2. Swap the email address.** Placeholder `hello@vaglo.example` appears in:
- `contact.html` — the form's `data-email` attribute and two `mailto:` links
- `index.html` and `system.html` — one footer `mailto:` each

Find them all:
```bash
grep -rn "vaglo.example" .
```

**3. Wire the form properly (recommended).** Right now, submitting opens the visitor's mail
client with everything pre-filled. That works, but it loses people who don't have a mail
client configured. To use a real endpoint — [Formspree](https://formspree.io) or
[Basin](https://usebasin.com), both free at low volume — edit `contact.html`:

```html
<form class="form" id="callform"
      data-endpoint="1"
      action="https://formspree.io/f/YOUR_ID"
      method="POST">
```

The `data-endpoint` attribute is what tells `app.js` to stop intercepting and let the form
POST normally.

**4. Review the numbers.** Every figure on the site is real and measured, taken from the
first working installation. They are presented unattributed ("a working installation at a
federal A/E firm") — no firm name, no solicitation numbers, no partner names, no client
project titles, and it should stay that way. Read the receipts section and the system page
once more with fresh eyes before launch and confirm you're comfortable publishing each one.

The figures used: 94 nights · 7,442 notices · 139 opportunities · 327 decisions · 61-page
package · 727 résumés · 586 person-project links · 5,997 tests · 136 completed plans ·
29 generator modules · 4 review passes · 20+ hours saved per SF330 package.

The "20+ hours saved" figure came from the first installation's own account of what an
SF330 used to take. It is the one number on the site sourced from a person rather than
from disk, so confirm you are happy standing behind it.

**5. Make an OG image.** There's no `og:image` yet, so links shared in email or Slack will
preview without a picture. A 1200×630 PNG of the hero — bone ground, green wordmark —
dropped at `assets/og.png`, then add to each page's `<head>`:

```html
<meta property="og:image" content="https://YOURDOMAIN/assets/og.png">
```

---

## Deploying

Any static host. Drag the folder onto [Netlify Drop](https://app.netlify.com/drop) or run:

```bash
npx vercel --prod
```

Then point your domain at it in the host's dashboard. No server, no database, nothing to
maintain.

## Working on it locally

```bash
python3 serve.py
```

Then open http://localhost:8747.

Use `serve.py`, not `python3 -m http.server`. The built-in server sends no cache headers at
all, so browsers apply their own guess and will happily serve you a stale `index.html` for
hours while you wonder why an edit did not take. `serve.py` is the same thing with
`Cache-Control: no-store` on every response.

Opening the files directly with `file://` mostly works, but some browsers block the fonts.

**On the real host**, do the opposite: cache `assets/` hard and `*.html` not at all. On
Netlify that is a `_headers` file:

```
/*.html
  Cache-Control: public, max-age=0, must-revalidate
/assets/*
  Cache-Control: public, max-age=31536000, immutable
```

Without that first rule a visitor who saw an old version can keep seeing it after you
deploy.

---

## Design notes

**Type** is Schibsted Grotesk via Google Fonts — one family, weights 400–700. Headlines run
at weight 400 with tight negative tracking; that light-large-headline treatment is what makes
the page read as modern rather than corporate. It's the one external request on the page; to
go fully self-contained, self-host the family in `assets/` and swap the `@import` at the top
of `styles.css`.

**Colour** is deep evergreen (`--brand: #295541`, taken straight from the logo file) on warm
bone paper (`--bg: #f2f0ed`) with near-black text. White on the green measures 8.5:1, past
WCAG AAA for body text. Amber and red are
reserved for meaning, never decoration. Every colour is a token in the `:root` block at the
top of `styles.css` — to reskin the whole site, edit that block and nothing else.

**Note the deliberate colour split:** the site chrome is green, but the mock dashboard defaults
to blue. That's not an inconsistency — it's the point. The mock is meant to read as *the
client's* colour, not ours, which is what makes the repainter demo land.

**The brand repainter** (`#mock`) is worth keeping intact because it carries the pitch: the
whole mock dashboard is driven by one CSS variable, `--b`. It isn't a gimmick — it's the same
mechanism the real product uses, which is why it's honest to demo it.

**Cache busting:** asset links carry a `?v=` query string. Bump it when you deploy a CSS or JS
change, or browsers will serve the old file.

## Copy rules that were followed

Worth keeping if you edit:
- No "AI-powered." Say what it does instead.
- Competitor *categories* only, never brand names.
- Every number on the page traces to something measured.
- The constraints section on `system.html` stays. Volunteering the limits is what makes the
  rest of the claims credible to a skeptical principal — it is a sales asset, not a
  disclaimer.
