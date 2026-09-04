# POC 8, explained simply

*A plain-language companion to
[poc8-connection-scene-findings.md](poc8-connection-scene-findings.md).
Everything here is the same story as the technical report — just told so
anyone can follow it.*

## What were we trying to do?

When someone asks our app *"show me how to connect Bose headphones to a
MacBook Air with the audio cable"*, we want to show them a **video**.

The problem: AI video generators are imaginative. Ask one to draw your exact
headphones and it draws *headphones-ish* — wrong buttons, invented logos,
cables plugged into places that don't exist. For a product-help app, a video
that *looks* right but *is* wrong is worse than no video at all.

POC 8 tested a way to make a video where **nothing can be imagined**:

1. Build a **3D twin** of each product — like a perfect digital action figure.
2. Put both twins in a 3D scene on a computer, with a little 3D cable.
3. Move the cable along a path we script ourselves — plug it in.
4. Press "render". The computer draws exactly what we set up. Nothing more.

It's like stop-motion animation with digital toys instead of clay. The AI
never gets to guess, because there is no AI in the loop — just a camera
pointed at a scene we built from facts.

## The safety rule we set before starting

Before the twins were allowed on stage, they had to pass two checks:

- **The measuring check:** does each twin match the product's real,
  documented measurements? (We know the MacBook is 30.41 cm wide because
  Apple says so — the twin must be too.)
- **The look-alike check:** we show a photo of the twin and a real official
  photo to a strict AI inspector and ask, "same product? right parts? nothing
  invented?" If the inspector says no — twice — everything stops.

And one hard rule: **if a check fails, we stop and write down why.** No
excuses, no fudging, no video.

## What actually happened

**Round 1.** The Bose twin passed both checks — it really looks like the
headphones. The MacBook twin failed badly: it looked like a paper-thin
squashed slab with junk stuck to it. Everything stopped, as designed.
(Cost so far: 3 cents.)

**Why did the Mac twin come out broken?** The twins are made by an AI
scanning service (Tripo3D): you give it photos from a few angles and it
sculpts a 3D model. Detective work showed the photos we fed it were a mess —
one showed the laptop *open*, another showed it *closed*, and one wasn't
even a photo, it was a diagram with arrows and labels drawn on it. The
sculptor was told to sculpt two different laptops at once. Garbage in,
garbage out.

**Round 2 — the re-scan.** The owner approved one more try with better
photos. We found Apple's own official picture set: sharp, clean, all showing
the *same open laptop* from the front and both sides. This time the sculptor
did much better: a believable open laptop, right shape, right proportions
(after we scaled it to the documented measurements — matching them almost
perfectly).

**But then the inspector caught something small and important.** The real
MacBook has one tiny headphone jack on its right side. The twin had **no
jack at all** — and instead had fake port shapes on the right side, copied
from the left side, where no ports exist. The sculptor understood the body
but *made up* the details. The inspector failed it. Everything stopped
again, as designed.

(Along the way we also found and fixed two bugs in **our own** photo-taking
setup: the twin looked see-through and too pale in our test photos because
of a lighting and transparency mistake in our rendering — like photographing
a dark blue laptop under stadium floodlights. Fixing that made our test
photos fair. It did not change the verdict: the missing jack is real.)

**Total spent across everything: $0.69 of a $10 budget.** No video was made,
nothing was published, and every attempt — including the failures — is
saved with receipts.

## What worked

- **The Bose twin** — passed and is ready to use.
- **The safety gates** — they caught a broken twin twice and stopped the
  project before we wasted money animating garbage. That's exactly their job.
- **The measuring repair** — scaling twins to documented sizes works
  beautifully.
- **The paper trail** — every attempt, cost, photo, and verdict is on file,
  including the failures.

## What didn't work

- **Scanning a laptop into a good-enough twin.** Two scans, and the second
  one used the best photos available anywhere — still no jack. The
  scanning AI is good at *bodies* and bad at *tiny details*. Unfortunately,
  "plug the cable into the tiny detail" is the whole video.

## The learnings

1. **Bad input photos ruin everything.** The single biggest jump in quality
   came from feeding the sculptor consistent, clean, official photos.
2. **Scanners sculpt the big shape, then improvise the details.** Ports,
   holes, buttons — the exact things instructions are about — are exactly
   what scanning gets wrong.
3. **Strict checking pays for itself.** The inspector caught things a quick
   human glance would forgive ("eh, looks like a MacBook"). Details are
   where wrong instructions hide.
4. **Failing cheap is winning.** We learned all of this for 69 cents because
   the checks come *before* the expensive steps.
5. **Keep every failure on file.** (We briefly lost one round's records when
   a rerun deleted its own history folder — that bug is fixed, and it taught
   us that the paper trail needs protecting too.)

## Takeaways — what happens next

- **Don't scan the MacBook a third time. Build it instead.** A closed
  MacBook is almost a simple rounded box. We know its exact measurements
  from Apple's specs, we know exactly where the jack goes from Apple's own
  port photo (which we saved), and we can paint the real photos onto the
  surfaces — a trick this project has already used successfully. That gives
  a twin with a *real* jack, costs nothing to generate, and passes the same
  checks or doesn't ship.
- **The Bose twin and the cable plan are ready** and waiting for the Mac.
- **Until then, the app's other proven video route** (real photos pinned at
  the start and end of each step, AI filling in only the motion, an
  inspector checking every clip) keeps working — it already produced our
  first approved-pending video.
- **The big idea survives:** videos people can trust are built from facts —
  measured twins, official photos, documented steps — with an inspector at
  every door and an honest "no video" whenever something can't be proven.
