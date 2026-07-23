# Interactive Video Product Understanding — High-Level Design

## The product in one sentence

**Point the system at any physical product, ask a question, and get a video
answer that updates when you ask a follow-up.**

The user may type, speak, share a product link, or show the product through a
photo or video. The answer is video by default: either an existing video segment
retrieved from the library or a new video generated through the Higgsfield API.
The active video can also include highlights, zooms, labels, comparisons, and
step indicators.

The system applies judgment about the answer form. If a question is fully
answered by a short factual reply—a weight limit, a spec number, a yes/no
compatibility fact—a concise text answer on the active surface is good enough,
and faster. Anything involving a part, an action, a state, a comparison, or a
spatial result is answered with video, because video is the easiest form for a
person to grasp. When in doubt, prefer video. For video answers, short labels,
captions, or citations may appear on or around the video, but the person must
be able to understand the core answer by watching the video itself.

---

## The key product idea

The product is a conversation with a video that understands the person’s
question and changes to answer each follow-up.

```text
POINT → ASK → WATCH THE ANSWER → ASK AGAIN → WATCH THE VIDEO UPDATE
```

The same video answer surface stays on screen across the conversation. Each
follow-up changes only what needs to change, so the person never loses their
place.

This is not:

- a chatbot that sometimes attaches a video;
- a manual search tool with citations;
- a passive library where the person must hunt through prerecorded videos;
- a new disconnected page or answer card for every question.

It is a **video product-understanding engine**. It can become the foundation for
interactive learning, onboarding, support, troubleshooting, commerce, and tools
for product manufacturers.

---

## What using it should feel like

A parent points their camera at a compact travel stroller. The system identifies
the exact model, and a product video becomes the active answer surface.

> **Person:** “Show me how to fold this for my flight.”  
> **Video:** A retrieved video shows the folding motion for that exact stroller
> model and highlights the first control to use.

> **Person:** “Will this stroller fit in the trunk of my Tesla Model Y?”  
> **Video update:** The system identifies the exact stroller and vehicle version,
> retrieves the stroller’s folded dimensions and the Tesla’s trunk opening and
> cargo dimensions, and uses a geometry engine to calculate whether it fits. The
> answer video shows the calculated placement inside the trunk.

> **Person:** “Show me a different position that could fit.”  
> **Video update:** The geometry engine calculates another valid orientation.
> The system retrieves a matching video or uses Higgsfield to generate the new
> position from the verified geometric layout.

> **Person:** “How do I know it is fully locked?”  
> **Video update:** The video focuses on the verified locked state and compares
> it with an incomplete fold.

> **Person:** “Now show me how to open it again.”  
> **Video update:** A retrieved or Higgsfield-generated video demonstrates the
> opening sequence for the same stroller.

The system remembers the product, the current view, the active step, what has
already happened, and what the person means by words such as “this,” “that,” or
“the other one.”

Higgsfield shows the computed result; it does not decide whether the stroller
fits. Exact dimensions and deterministic geometry make that decision.

---

## The product promise

The experience should make five promises:

1. **The answer is video by default.** A question fully answered by a short
   fact may receive a concise text reply, but anything visual, procedural, or
   spatial is answered with video. When in doubt, prefer video.
2. **Follow-ups update the active video immediately.** Do not make the person
   restart or read through a new wall of text.
3. **The product stays recognizable.** Preserve the same object and view unless
   changing the view helps answer the question.
4. **The video is truthful.** Buttons, parts, motions, and product behavior must
   match trustworthy evidence.
5. **Uncertainty is visible.** If the system is unsure, the video experience asks
   for the missing angle, label, state, or choice instead of pretending.

---

## The video is the answer

The app has two main areas:

```text
+---------------------------------------------------------------+
|                                                               |
|                    ACTIVE ANSWER VIDEO                        |
|                                                               |
|      product · highlights · labels · motion · steps           |
|      comparisons · current state · expected state             |
|                                                               |
|             [small source/citation indicators]                |
|                                                               |
+---------------------------------------------------------------+
| Ask by voice or text...                              [camera]  |
+---------------------------------------------------------------+
```

Chat history may be available when needed, but it is secondary. The active video
is where the answer lives.

The video can answer in several ways:

| Video operation | Example |
|---|---|
| Point and highlight | Show the stroller’s fold-release control. |
| Label | Name every visible control. |
| Zoom and reframe | Move closer to the release mechanism. |
| Animate an action | Show press, hold, turn, slide, or connect. |
| Show steps | Move through setup one video step at a time. |
| Compare states | Fully locked fold versus an incomplete fold. |
| Compare products | Show important differences side by side. |
| Show spatial fit | Place the folded stroller in the Tesla trunk at a computed orientation. |
| Reveal internals | Use a verified diagram to show what cannot be seen outside. |
| Ask visually | Circle two similar parts and ask which one the person has. |

The first source for an answer is an existing trustworthy video. This can be
an approved source video or a previously generated video that already passed
verification. The system retrieves the most relevant segment—not merely a link
to a whole video—and plays that segment as the answer. If existing videos cannot
answer the exact question, the system generates the missing video through the
**Higgsfield API**, verifies it, presents it, and saves it for future reuse.

---

## The whole system on one page

```text
                 PERSON AND PHYSICAL PRODUCT
           voice · text · link · photo · live video
                              |
                              v
               +-----------------------------+
               |     ACTIVE VIDEO PLAYER     |
               | persistent video answer and |
               | immediate video updates     |
               +-------------+---------------+
                             ^ |
                    update   | | follow-up
                             | v
       +-----------------------------------------------+
       |          UNDERSTANDING ORCHESTRATOR           |
       | What does the person mean, and what video     |
       | will answer them most clearly?                |
       +--------+----------------+----------------+-----+
                |                |                |
                v                v                v
       +----------------+ +--------------+ +--------------+
       | Product and    | | Trusted      | | Session and  |
       | scene identity | | evidence     | | video state  |
       +--------+-------+ +------+-------+ +------+-------+
                |                |                |
                +----------------+----------------+
                                 |
                                 v
                     +------------------------+
                     | VIDEO ANSWER PLANNER   |
                     | decide what the answer |
                     | video must demonstrate |
                     +-----------+------------+
                                 |
                                 v
                    +--------------------------+
                    | RETRIEVE EXISTING VIDEO  |
                    | approved + saved videos  |
                    | search · choose segment  |
                    | clip · crop · reframe    |
                    +------------+-------------+
                                 |
                         answers the question?
                            /           \
                          yes            no
                           |              |
                           |              v
                           |   +--------------------------+
                           |   | GENERATE WITH HIGGSFIELD |
                           |   | create missing video     |
                           |   +------------+-------------+
                           |                |
                           +----------------+
                                 |
                                 v
                     +------------------------+
                     |       VERIFIER         |
                     | product · facts ·      |
                     | appearance · action    |
                     +-----------+------------+
                                 |
                                 v
                    update the active video
                                 |
                  if newly generated and verified
                                 |
                                 v
                    save + index for future reuse
```

The important architectural rule is **retrieve first, generate second**. A
follow-up first searches the indexed video library for a segment that directly
answers the new question. If no segment passes the relevance and correctness
checks, Higgsfield generates the missing video. While that answer is being built,
the active video surface reacts immediately so the experience never looks
frozen.

---

## The system maintains a video answer state

The active video experience is stored as structured information, not as one
fixed video file. Think of it as a video player with controllable layers.

```text
Video Answer State
├── active retrieved or generated video
├── known product parts and their locations
├── camera position, crop, and zoom
├── current question and goal
├── active highlights and labels
├── current instruction step
├── expected product state
├── animation or motion instructions
├── evidence connected to each visual fact
├── uncertainty and requested user input
└── pending retrieved or Higgsfield-generated video
```

When a follow-up arrives, the system first updates the active video state instead
of rebuilding the whole page. It also remembers which retrieved or generated video
answered each earlier question:

```text
Follow-up: “Show me a different position that could fit.”

Video update:
  focus        = Tesla trunk
  placement    = next geometry-approved orientation
  camera       = wide enough to show clearances
  highlight    = tightest clearance points
  keep         = exact stroller, exact car, dimensions, verified fit result
  remove       = previous placement
```

Because the video answer has controllable layers, this update can feel immediate
and smooth. It also preserves the person’s mental map of the product.

Each video-answer state is saved. The user can move backward, replay a step, or ask
the system to show the difference between two states.

---

## Retrieve first; generate only when retrieval is not enough

Every question that warrants a video answer follows one clear video-source
policy:

```text
1. Search existing videos for an exact answer
                       |
                       v
2. Select and clip the best matching moment
                       |
               does it fully answer?
                  /           \
                yes            no
                 |              |
                 v              v
          show retrieved     generate missing
          video answer       video with Higgsfield
                 |              |
                 +------+-------+
                        v
                 verify and show
```

Retrieval is the first choice because an existing trustworthy demonstration is
faster, cheaper, and less likely to change the product incorrectly. Generation
exists to answer questions that the video library does not already cover.

For a video-worthy question, both routes end in a video; a failed retrieval
falls through to generation rather than to text. Only if generation also fails
does the system keep the current verified video, show visible uncertainty, and
offer the best evidence-backed text answer it can—an honest fallback is better
than leaving the person with nothing.

### Primary path: retrieve an existing video answer

Official, otherwise approved, and successfully verified generated videos are
processed and indexed. The system stores searchable segments with information
such as:

- exact product and model;
- parts and controls shown;
- action being demonstrated;
- product state before and after the action;
- start and end timestamps;
- viewpoint and visual quality;
- source, rights, and evidence links;
- whether the video was retrieved or generated;
- the verification result and when it was checked.

For a follow-up, retrieval searches this segment index, chooses the smallest
piece that answers the question, and adapts it to the active video with crops,
highlights, labels, or playback controls when useful.

The target experience is:

```text
follow-up asked
      |
      v
active video reacts immediately
      |
      v
retrieved video answer begins in about one second or less
```

### Fallback path: generate only when the answer type is safe to generate

If no retrieved segment fully answers the question, the planner first classifies
what the missing visual must prove. Prompt-only Higgsfield generation is **not
allowed for product-operation instructions** such as folding, installing,
unlocking, repairing, or pressing an exact control. In a controlled three-run
Ready2Jet test, the prompt and settings were applied exactly, but 0/3 videos
showed the real mechanism or any fold; all three changed the stroller into a
different open product.

For those instructions, the fallback remains visual: show official diagrams or
an approved image sequence with highlights, retrieve a human-demonstrated clip,
or use a deterministic renderer when the mechanism can be represented exactly.
Higgsfield may generate a candidate offline, but it cannot become an answer
unless an action verifier or human reviewer proves every required step.

Higgsfield remains a candidate for lower-risk transitions and visual polish
when verified start/end states constrain the result and the invented motion is
not itself the instruction.

```text
no adequate video segment
          |
          v
classify whether generation is safe for this answer
          |
     safe +---- exact operation → official visual sequence,
          |                       retrieved demonstration,
          |                       or deterministic rendering
          v
build constrained Higgsfield candidate
          |
          v
verify product appearance and demonstrated action
          |
     pass +---- fail → retry safely or show visible uncertainty
          |
          v
play generated answer in the active video player
          |
          v
save, tag, embed, and index it for future questions
```

The video player changes immediately to acknowledge the follow-up and preserve the
current product, focus, and step while the answer is prepared. A generated
candidate replaces that temporary visual state only after it passes
verification. A failed or unverifiable candidate is never shown as instruction.

This is **progressive video answering**: react immediately, retrieve whenever
possible, and generate only what is missing.

---

## Every successful generation grows the video library

Higgsfield should never generate the same verified answer twice when the system
can safely reuse the first result.

```text
question has no matching video
             |
             v
generate with Higgsfield
             |
             v
does it correctly answer the question?
        /                 \
      no                   yes
      |                     |
reject or retry             v
                    play it as the answer
                             |
                             v
                 store video in object storage
                             |
                             v
                 save searchable record in DB
                             |
                             v
                  future retrieval can reuse it
```

The database record should include:

- exact product and version;
- question meaning or intent;
- product part, action, and before/after state;
- viewpoint and visual format;
- source evidence used to create it;
- Higgsfield generation settings and reference assets;
- verification score and verifier version;
- creation date, usage count, and last successful use;
- access scope and reuse rights;
- a fingerprint for duplicate detection.

The video file itself belongs in object storage; the database stores its location
and searchable facts. People can reasonably describe the same question in many
ways, so retrieval should match meaning rather than only identical wording.

A saved video becomes a candidate, not permanent truth. If the product version,
supporting evidence, safety rules, or verification system changes, the asset is
rechecked before reuse. Failed or uncertain generations are never added to the
trusted retrieval pool.

---

## The reasoning loop

Every new question or follow-up runs the same loop:

```text
UNDERSTAND → FIND EVIDENCE → PLAN VIDEO → RETRIEVE VIDEO
      ^                                      |
      |                              adequate segment?
      |                                 /         \
      |                               yes          no
      |                                |            |
      |                                |      HIGGSFIELD
      |                                |            |
      |                                +-----+------+
      |                                      |
      |                                VERIFY VIDEO
      |                                      |
      +---------- next follow-up ← UPDATE ACTIVE VIDEO
```

### 1. Understand the product and the person’s reference

The system determines:

- the exact product and version;
- what is visible in the current view;
- which part “this,” “it,” or “the other one” refers to;
- what the person wants to learn or do;
- what the active video currently shows;
- whether the question needs a video demonstration or is fully answered by a
  short factual reply (defaulting to video when unsure).

If two products or parts are too similar, the video player can circle the candidates
and ask the person to choose.

### 2. Find trustworthy evidence

The system retrieves facts and procedures for grounding, then searches existing
videos for a segment that answers the exact question on video. Search combines
exact matching for model numbers and error codes with meaning-based and visual
search for natural questions.

The evidence may come from manufacturer manuals, official support pages,
official video and media, trustworthy product databases, verified dimension
specifications, or the person’s current camera view.

### 3. Plan the video answer

The planner does not first write a paragraph. It produces a video plan:

```text
User goal: Check whether the folded stroller fits in a Tesla Model Y trunk
Inputs: Exact stroller version + exact Model Y version
Verified facts: Folded stroller dimensions + trunk opening/interior dimensions
Calculation: Deterministic geometry and collision checks
Result: Fits or does not fit, with clearance and valid orientations
Existing-video query: Exact products + verified valid placement
Generation fallback: Higgsfield grounded with computed geometry and references
Optional words: “Fits in this orientation”
Evidence: Official dimensions and source links
```

### 4. Verify the truth of the video

The verifier checks:

- Is this the exact product and model?
- Is the highlighted part really the fold-release control on this exact model?
- Does the evidence support the instruction?
- Does the shown movement match the real action?
- Does the expected result match the documentation?
- Are both sets of dimensions from the exact product versions?
- Does the video show an orientation that passed the geometry calculation?
- Is the answer safe at the current confidence level?

A correct citation attached to an incorrect video is still a failure.

### 5. Update the active video

The player applies the new retrieved or generated answer while preserving the
product and conversation context. Transitions show the person what changed
without resetting the experience.

---

## The product knowledge behind the video

The system needs more than text chunks from manuals. It needs a connected
**product evidence graph**:

```text
Product
├── versions and model aliases
├── visible parts and their locations
├── controls and possible actions
├── states, lights, sounds, and error conditions
├── procedures and ordered steps
├── exterior, folded, opening, and interior dimensions
├── shapes, clearances, and valid spatial orientations
├── compatible products and accessories
├── official images, diagrams, and video moments
└── evidence source for every fact and relationship
```

This graph lets the video planner answer questions such as:

- Where should the arrow point?
- What should move?
- What changes after the action?
- Which next step is valid?
- Can one exact product fit inside another?
- Which computed positions are valid and collision-free?
- What should remain unchanged in the visual?

Sources are saved as dated snapshots and labeled by product version, region,
language, and firmware when relevant. Old information is not silently treated as
current truth.

---

## Main building blocks

| Building block | Plain-language job |
|---|---|
| Active Video Player | Plays the current answer video and applies smooth follow-up updates. |
| Voice/Text/Camera Input | Lets the person point and ask naturally. |
| Understanding Orchestrator | Decides what the person means and what capability acts next. |
| Product and Scene Resolver | Identifies the exact product, parts, view, and visible state. |
| Session Memory | Remembers the goal, prior steps, references, and video-answer history. |
| Evidence Retriever | Finds trustworthy facts and media for the exact question. |
| Product Evidence Graph | Connects products, parts, actions, states, procedures, and sources. |
| Dimension Resolver | Retrieves and normalizes exact product, opening, and interior measurements. |
| Deterministic Fit Engine | Calculates whether objects fit and returns valid positions; it does not use video generation to guess. |
| Video Answer Planner | Defines what the answer video must show and demonstrate. |
| Video Compositor | Applies highlights, labels, zooms, transitions, and player-state changes. |
| Video Retrieval Engine | Searches approved and previously verified generated videos for an exact answer. |
| Higgsfield Generator | Creates the missing video answer only when retrieval cannot. |
| Generated Video Library | Stores, indexes, and reuses successful Higgsfield answers. |
| Verifier | Checks factual support, product fidelity, action correctness, and safety. |
| Evaluation System | Replays visual conversations and catches regressions. |

The orchestrator is the conductor, not the video renderer. The video planner
creates a structured answer plan. Deterministic client and server code updates
the player. Higgsfield supplies the generated fallback when retrieval cannot
produce an adequate video answer.

---

## How the related use cases fit

Use case #1—Interactive Product Understanding—is the video-first platform.

| Use case | How it appears in the video product | Decision |
|---|---|---|
| Visual Troubleshooting | The answer video compares observed and expected states, asks visual questions, and guides one verified step at a time. | A major feature after the core interaction works. |
| Compatibility Resolver | Two products appear together with compatible and incompatible connection points highlighted. | A later capability module. |
| Decision Intelligence | Products and trade-offs appear in an interactive visual comparison driven by the user’s constraints. | A later application surface. |
| Physical Fit Engine | Deterministic geometry decides whether exact products fit; the video layer shows the result and alternate valid positions. | Include as a capability in the stroller demo, while keeping its calculation separate from Higgsfield. |

---

## The first travel-stroller demonstration

The first demo should prove the video interaction with a task where movement,
viewpoint, and follow-ups matter.

### Demo flow

1. A parent shares a compact travel stroller photo, video, or product page.
2. The system identifies the exact model and loads its current answer video.
3. “Show me how to fold this for my flight” retrieves the best matching segment
   and demonstrates the verified fold sequence.
4. “Will the folded stroller fit in the trunk of my Tesla Model Y?” resolves the
   exact car version and retrieves verified dimensions for both products.
5. The deterministic fit engine checks the trunk opening, interior space,
   collisions, and clearance. It returns a fit result and valid orientations.
6. The active video shows the computed stroller placement inside the trunk.
7. “Show me a different position that could fit” asks the fit engine for another
   valid orientation rather than asking Higgsfield to guess.
8. The system retrieves a matching video or generates the missing placement with
   Higgsfield using the computed orientation as a constraint.
9. The verifier checks that the video matches the dimensions and valid placement.
10. Every successful Higgsfield video is saved and becomes retrievable later.
11. The parent can replay, compare valid positions, or continue asking.

Every follow-up should produce a visible response immediately. In the controlled
POC, each 5.37-second `dop-preview` clip took about 6 minutes 32 seconds to
arrive. Therefore, the immediate response must come from retrieval, cached
generated assets, or an evidence-backed temporary visual state—not live
generation. A new candidate can replace it later only after verification.

---

## Recommended build order

| Phase | Build | What it proves |
|---|---|---|
| 1 | One travel-stroller model, one Tesla Model Y version, verified dimensions, a small approved video set, and 20 questions | The product and evidence model is sufficient. |
| 2 | Video segmentation, indexing, retrieval, clipping, and playback in a persistent player | Existing videos can become direct answers. |
| 3 | Orchestrator that converts questions into structured video plans and retrieval queries | Natural language can retrieve the right answer video. |
| 4 | Immediate player transitions plus session state, reference resolution, replay, and undo | Follow-ups update the active video without losing context. |
| 5 | Dimension normalization and deterministic 3D fit calculation with alternate orientations | Fit answers and placements are mathematically valid. |
| 6 | Safe-generation lanes: deterministic or official visuals for exact operations; Higgsfield only for constrained, verifiable, lower-risk candidates | Missing visuals do not turn into believable-but-wrong instructions. |
| 7 | Save, tag, embed, deduplicate, and retrieve every successful generated video | Generation makes future answers faster and cheaper. |
| 8 | Safe automated ingestion and freshness checks for product evidence, dimensions, and videos | New products can be added reliably. |
| 9 | URL, photo, and video product identification | The experience can start from real-world inputs. |
| 10 | Visual troubleshooting and other application modes | The core video-first platform supports broader use cases. |

The early MVP should prove reliable video retrieval, deterministic visual
results, playback updates, and offline verification of any Higgsfield candidate.
Prompt-only generation of operating instructions is outside the safe MVP path.
Fast, consistent video updates are the product’s core magic.

---

## What to measure

The evaluation set must score entire visual conversations.

- Did the system identify the exact product and visible parts?
- Did it choose the right answer form—concise text for a simple fact, video for
  anything visual, procedural, or spatial?
- Did the video point to the correct location?
- Did the motion demonstrate the correct action?
- Did every fact shown in the video have supporting evidence?
- Were the stroller and trunk dimensions from the exact product versions?
- Did the deterministic fit result account for the trunk opening, interior
  shape, clearance, and collisions?
- Did every shown alternate position pass the geometry calculation?
- Did a follow-up update the active video instead of starting over?
- Did stable parts stay stable across updates?
- Did the transition make the change easy to understand?
- Did the first useful video update appear quickly?
- Did the retrieved or generated answer start without unnecessary delay?
- Did retrieval reuse an existing verified generated answer when possible?
- What percentage of questions required a new Higgsfield generation?
- Did every successful generation become searchable for the next request?
- Did the system ask for missing camera evidence when uncertain?
- Did it preserve context across several follow-ups?
- Did it refuse to display an unverified or unsafe instruction?

Key latency measures should include time to first player reaction, time to a
retrieved answer video, and time to a verified Higgsfield answer.

---

## Trust and safety rules

1. Every highlighted part, state, movement, and instruction must connect to
   evidence or clearly display uncertainty.
2. Generated videos are checked for both product appearance and demonstrated
   action before becoming the active answer.
3. Only successful, verified Higgsfield outputs enter the reusable video pool.
   Saved assets retain their evidence, generation, and verification provenance.
4. High-risk procedures require stronger product identity and source confidence.
5. Higgsfield must visualize a computed fit result; it must never decide whether
   the stroller fits or invent an unverified position.
6. The video must not hide uncertainty behind a polished animation.
7. Downloaded documents and pages are untrusted data, never commands to the AI.
8. Uploaded photos, videos, and conversation history have clear access,
   retention, and deletion controls.
9. A failed generation must preserve the current verified video and show visible
   uncertainty instead of inventing an answer. It may offer an evidence-backed
   text answer as a fallback, clearly marked as such.
10. Prompt-only generated video is prohibited for exact product-operation
    instructions. Those answers require retrieved real demonstrations, official
    visual steps, or deterministic rendering. A future generative path must pass
    a separately validated action-verification gate before this rule changes.

---

## Where the lasting advantage comes from

The defensible system is not just a language model or a video generator. It is:

- a product graph that knows exact models and parts;
- an evidence graph connecting parts, actions, states, procedures, and sources;
- normalized dimensions and deterministic spatial reasoning;
- a video state model that survives across follow-ups;
- a planner that turns questions into precise answer-video requirements;
- a growing library of previously generated and verified video answers;
- a fast player and compositor for smooth follow-up updates;
- verification that checks both factual and video truth;
- evaluation data from real video conversations.

In simple terms:

> **The model understands the question. The product graph knows the object. The
> evidence graph knows what is true. Retrieval reuses what already works.
> Higgsfield creates only what is missing. The video shows the answer.**

---

## Final summary

Interactive Video Product Understanding turns a physical product into a living
video conversation.

The person points, asks, watches, and follows up. The answer lives in one
persistent video player. Each follow-up updates the active video. The system
retrieves an existing video answer first. When none can answer, it generates the
missing video through the Higgsfield API. Every successful generated answer is
saved, indexed, and reused so the library becomes more capable over time. Short
factual questions may receive a concise text reply, but video remains the
default because it is the easiest form for a person to grasp.

The stroller-folding and Tesla-trunk fit flow is the first proof. The larger
product is the reusable
engine that understands a product, grounds the answer in evidence, and turns
every question into a trustworthy video answer.
