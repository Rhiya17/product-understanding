# Higgsfield Video Experiments: Can We Trust It to Make Our Videos?

## Why are we doing this?
Imagine you have a question about a product, like "Will this stroller fit in my car?" or "How do I fold this stroller with one hand?" Instead of reading a long, boring manual, our app wants to show you a **short, helpful video**. 

Sometimes, that video doesn't exist yet, so we use an AI video generator called **Higgsfield** to create the video on the spot. 

**But there's a big problem:** Higgsfield loves to use its imagination. If you ask Higgsfield to show a stroller folding, it might invent fake buttons or change the stroller entirely. If the video lies to you, you might break your stroller or buy one that doesn't fit in your car! 

So, we ran two experiments (called "Proof of Concepts" or POCs) to see if we can force Higgsfield to tell the truth.

---

## Experiment 1: Fitting a Stroller Box in a Trunk

### The Goal 🎯
We want to know if a folded stroller (shaped like a box) fits inside a Tesla car trunk. We already did the math and know *exactly* where it fits. But Higgsfield doesn't understand math or measurements. We wanted to see if we could draw a picture of the box in the trunk, give it to Higgsfield, and have Higgsfield turn it into a realistic video *without moving the box or changing its size*.

### Test A: "Please hold still" (Failed ❌)
First, we drew a picture of our blue box inside the gray trunk:
* 🖼️ [Our starting drawing (The Truth)](../poc-higgsfield-geometry/out/placement_0.png)

We gave this picture to Higgsfield and told it in words: *"Spin the camera smoothly around, but keep the objects perfectly still."*
* 🎥 **Watch the video:** [e2_orbit.mp4](../poc-higgsfield-geometry/out/e2_orbit.mp4)

**Why it failed:** Telling Higgsfield "don't move anything" is like telling a puppy to stay still. For the first 1.5 seconds ([frame_004.png](../poc-higgsfield-geometry/out/e2_orbit_frames/frame_004.png)), it behaved. But by 3.5 seconds ([frame_008.png](../poc-higgsfield-geometry/out/e2_orbit_frames/frame_008.png)), Higgsfield got bored and started inventing things! It turned the car trunk into a fancy glass display case on a pedestal, and our solid blue box melted into an open tray ([frame_011.png](../poc-higgsfield-geometry/out/e2_orbit_frames/frame_011.png)).

### Test B: The "First and Last Frame" Trick (Success! ✅)
Next, we tried a secret trick. Instead of giving Higgsfield just one picture and some words, we gave it **two pictures**:
1. A drawing of the box at the start ([placement_0.png](../poc-higgsfield-geometry/out/placement_0.png))
2. A drawing of the box at the end ([placement_1.png](../poc-higgsfield-geometry/out/placement_1.png))

We told Higgsfield: *"Just connect these two pictures."*
* 🎥 **Watch the video:** [e5_firstlast.mp4](../poc-higgsfield-geometry/out/e5_firstlast.mp4)

**Why it worked:** Because we "pinned" the video at the start and the end with our own truthful drawings, Higgsfield wasn't allowed to invent glass domes or pedestals. It smoothly animated the transition from start to finish ([frame_006.png](../poc-higgsfield-geometry/out/e5_firstlast_frames/frame_006.png)), ending exactly where we wanted it to ([frame_011.png](../poc-higgsfield-geometry/out/e5_firstlast_frames/frame_011.png)).

**The Lesson:** Never trust Higgsfield to decide where things go. Do the math yourself, draw the start and end pictures yourself, and just let Higgsfield animate the in-between parts!

---

## Experiment 2: The One-Hand Stroller Fold

### The Goal 🎯
Imagine trying to teach someone a magic trick by sending them a picture of you holding some cards and texting them: *"Slide your thumb and squeeze."* They'd probably do it wrong.

In this experiment, we wanted to see if we could give Higgsfield one real photo of a stroller and written instructions on how to fold it with one hand. We wanted to see if Higgsfield could figure out the mechanics and create a truthful video of the stroller folding.
* 🖼️ [Our starting photo (The Input)](../poc-higgsfield-one-hand-fold/references/start-frame.png)

### The First Try (Sneaky Settings ❌)
We wrote very careful instructions: *"keep the camera still, use one hand, push the thumb switch, squeeze the lever."*
* 🎥 **Watch the video:** [ready2jet-one-hand-fold.mp4](../poc-higgsfield-one-hand-fold/out/ready2jet-one-hand-fold.mp4)
* 🖼️ [See the breakdown step-by-step](../poc-higgsfield-one-hand-fold/out/contact-sheet.png)

**Why it failed:** It was a disaster! The stroller didn't fold. Instead, Higgsfield morphed it into a totally different stroller. Fake red buttons appeared, the person used *both* hands instead of one, and the camera swooped all over the place. We found out Higgsfield's server had secretly rewritten our instructions and added the camera swoop behind our backs!

### The Corrected Test (Still Failed ❌)
We turned off Higgsfield's sneaky settings, locked the camera in place, and ran the test 3 times to be fair. 
* 🖼️ [See the breakdown of all 3 tries](../poc-higgsfield-one-hand-fold/out/corrected-three-contact-sheets.png)

**Why it failed:** 0 out of 3 videos worked. Even with perfect instructions, Higgsfield just changed the small stroller into a bigger stroller that stayed completely open. It never folded.

**The Lesson:** Higgsfield has watched millions of stroller videos, but it doesn't know how the hidden gears and buttons on *this specific stroller* work. Words are too vague. If you ask Higgsfield to show a mechanical action, it will just guess—and it will usually guess wrong. For things like this, we should just show the user real, recorded videos instead of letting Higgsfield guess!

---

## Three More Things We Learned Along the Way

### 1. Higgsfield is slow ⏳
Every 5-second video took **3 to 7 minutes** to make. There is no "fast mode"—you drop off your order and come back later, like film development, not like a Polaroid. Our product plan assumed a new video "may take a few seconds," but reality is 40–80× slower. Nobody will stare at a loading spinner for 6 minutes!

**What this means:** the instant answers must come from videos we **already have** (real videos, or Higgsfield videos we made and checked earlier). The predictable ones—folding, unfolding, trunk positions—should be made ahead of time, so the user almost always gets a ready-made video right away.

### 2. Higgsfield has sneaky default settings 🕵️
Unless you explicitly tell it not to, Higgsfield's server secretly **rewrites your instructions** into different words you never see, and **adds a random camera swoop at full strength** that you never asked for. This ruined our first stroller test without us knowing.

**What this means:** always switch off the instruction-rewriter and set the camera motion yourself, or Higgsfield changes your experiment (and your product's answers) behind your back.

### 3. You can only hand Higgsfield pictures and words ✋
Officially, Higgsfield accepts just: **one picture** (which must live on a public web link—no file uploads) and **one text description**. You can pick a speed/quality tier (lite, preview, or turbo) and a video length, and that's it. But we discovered a **hidden, undocumented mode** called `first-last-frame` that accepts **two pictures**—the first frame AND the last frame of the video. That secret mode is what made Experiment 1's Test B succeed.

Either way, there is **no way** to give it measurements, coordinates, or 3D shapes.

**What this means:** if our math figures out "the stroller fits at exactly this angle," there is no input slot to tell Higgsfield that. The only way to get truth into the video is to **draw the answer into the pictures ourselves** and pin the video down with them—one picture pins the start, and the hidden mode lets us pin the ending too.
