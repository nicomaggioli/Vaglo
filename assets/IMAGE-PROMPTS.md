# Image prompts

Three slots on the homepage. Save into `assets/` with these exact names.

| File | Section headline |
|---|---|
| `feature-brief.jpg`     | Stop reading solicitations at midnight |
| `feature-selection.jpg` | Your strongest projects, picked for you |
| `feature-review.jpg`    | Nothing goes out with a hole in it |

Export **1600 x 1200** (4:3), JPG, 200 to 400KB.

---

## Read this before you generate anything

The reference shot has the product on the laptop screen. **That is a composite.** No image
model can render your dashboard, and anything it invents will be garbled fake UI that a
careful buyer notices immediately. It is the single fastest way to look untrustworthy on a
page whose whole argument is that you do not fake things.

So it is two steps:

1. Generate the photograph with a **blank, bright screen**. Every prompt below says so.
2. Drop a real screenshot of the dashboard onto that screen afterwards.

Step two takes about five minutes in Figma, Photoshop, Keynote or Canva: place the
screenshot over the screen area, use a four-corner distort or perspective warp to match the
laptop angle, then drop it to roughly 90% opacity so a little of the screen glare shows
through. That last touch is what stops it looking pasted on.

If you would rather skip the compositing, tell me and I will render the dashboard at the
angles these shots need, or shoot it in a browser mockup frame instead.

---

## 1. feature-brief.jpg

> Close up of a person's hands typing on an open laptop on a white desk, seen from behind
> and slightly to the side, the laptop screen bright and blank and white, a ceramic mug of
> coffee and a cup of pencils blurred in the foreground, a small potted plant and a softly
> blurred bright window in the background, warm morning daylight, shallow depth of field,
> shot on 50mm at f1.8, natural lifestyle photography, warm neutral palette, no text or
> interface on the screen

## 2. feature-selection.jpg

> Two colleagues at a desk in a bright office, one seated at an open laptop and one standing
> and leaning in to point at the screen, the laptop screen bright and blank and white,
> printed drawings and project sheets spread on the desk beside them, large window with soft
> daylight behind, shallow depth of field, shot on 35mm, natural documentary photography,
> warm neutral palette, no text or interface on the screen

## 3. feature-review.jpg

> An open laptop on a wooden desk turned three quarters to camera, the screen bright and
> blank and white, a thick bound printed document open beside it next to reading glasses and
> a pen, warm daylight from the left, shallow depth of field, foreground softly out of
> focus, shot on 85mm, quiet and precise, warm neutral palette, no text or interface on the
> screen

---

## Getting a usable frame

**Say "blank white screen" and mean it.** If the model puts an interface on there, discard
the image. Do not try to cover bad UI with your screenshot; the glow and reflections will
not match.

**Hands are the other failure point.** Ask for them at the edge of frame, from behind, or
resting rather than mid-gesture. Check finger counts before you commit to a frame.

**One light source.** A single window. Two or more and it starts to look rendered.

**Leave room around the laptop.** You need margin for the four-corner warp, and a screen
that runs off the edge of frame is much harder to composite onto.

**Generate four to six of each.** Keep the boring one. Photos that try hard read as stock,
and this buyer is unusually good at spotting stock.

Midjourney: append `--ar 4:3 --style raw`. For the compositing step, any editor with a
perspective or free transform will do.

**Faces need permission** if the person is recognisable. All three prompts are framed so
that shooting over the shoulder, from behind, or cropped at the chin still works.

---

## The image worth more than these three

A photograph of **a real finished package**, redacted. Sixty one pages of tabbed, printed
proposal, stacked or fanned across a desk in daylight. No compositing, no AI, nothing to
fake. It proves the one thing nobody else in the category can show, and it is what would
let the hero button become "See a finished package" instead of "Request a call".
