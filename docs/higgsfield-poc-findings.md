# AI Video Experiments: Can We Trust a Robot to Make Videos?

## Why are we doing this?
Imagine you have a question about a product, like "Will this stroller fit in my car?" or "How do I fold this stroller with one hand?" Instead of reading a long, boring manual, our app wants to show you a **short, helpful video**. 

Sometimes, that video doesn't exist yet, so we use an AI (a smart robot) called **Higgsfield** to generate the video on the spot. 

**But there's a big problem:** AIs love to use their imagination. If you ask an AI to show a stroller folding, it might invent fake buttons or change the stroller entirely. If the video lies to you, you might break your stroller or buy one that doesn't fit in your car! 

So, we ran two experiments (called "Proof of Concepts" or POCs) to see if we can force the AI to tell the truth.

---

## Experiment 1: Fitting a Stroller Box in a Trunk

### The Goal 🎯
We want to know if a folded stroller (shaped like a box) fits inside a Tesla car trunk. We already did the math and know *exactly* where it fits. But the AI doesn't understand math or measurements. We wanted to see if we could draw a picture of the box in the trunk, give it to the AI, and have the AI turn it into a realistic video *without moving the box or changing its size*.

### Test A: "Please hold still" (Failed ❌)
First, we drew a picture of our blue box inside the gray trunk:
* 🖼️ [Our starting drawing (The Truth)](../poc-higgsfield-geometry/out/placement_0.png)

We gave this picture to the AI and told it in words: *"Spin the camera smoothly around, but keep the objects perfectly still."*
* 🎥 **Watch the video:** [e2_orbit.mp4](../poc-higgsfield-geometry/out/e2_orbit.mp4)

**Why it failed:** Telling the AI "don't move anything" is like telling a puppy to stay still. For the first 1.5 seconds ([frame_004.png](../poc-higgsfield-geometry/out/e2_orbit_frames/frame_004.png)), it behaved. But by 3.5 seconds ([frame_008.png](../poc-higgsfield-geometry/out/e2_orbit_frames/frame_008.png)), the AI got bored and started inventing things! It turned the car trunk into a fancy glass display case on a pedestal, and our solid blue box melted into an open tray ([frame_011.png](../poc-higgsfield-geometry/out/e2_orbit_frames/frame_011.png)).

### Test B: The "First and Last Frame" Trick (Success! ✅)
Next, we tried a secret trick. Instead of giving the AI just one picture and some words, we gave it **two pictures**:
1. A drawing of the box at the start ([placement_0.png](../poc-higgsfield-geometry/out/placement_0.png))
2. A drawing of the box at the end ([placement_1.png](../poc-higgsfield-geometry/out/placement_1.png))

We told the AI: *"Just connect these two pictures."*
* 🎥 **Watch the video:** [e5_firstlast.mp4](../poc-higgsfield-geometry/out/e5_firstlast.mp4)

**Why it worked:** Because we "pinned" the video at the start and the end with our own truthful drawings, the AI wasn't allowed to invent glass domes or pedestals. It smoothly animated the transition from start to finish ([frame_006.png](../poc-higgsfield-geometry/out/e5_firstlast_frames/frame_006.png)), ending exactly where we wanted it to ([frame_011.png](../poc-higgsfield-geometry/out/e5_firstlast_frames/frame_011.png)).

**The Lesson:** Never trust the AI to decide where things go. Do the math yourself, draw the start and end pictures yourself, and just let the AI animate the in-between parts!

---

## Experiment 2: The One-Hand Stroller Fold

### The Goal 🎯
Imagine trying to teach someone a magic trick by sending them a picture of you holding some cards and texting them: *"Slide your thumb and squeeze."* They'd probably do it wrong.

In this experiment, we wanted to see if we could give the AI one real photo of a stroller and written instructions on how to fold it with one hand. We wanted to see if the AI could figure out the mechanics and create a truthful video of the stroller folding.
* 🖼️ [Our starting photo (The Input)](../poc-higgsfield-one-hand-fold/references/start-frame.png)

### The First Try (The Sneaky Robot ❌)
We wrote very careful instructions: *"keep the camera still, use one hand, push the thumb switch, squeeze the lever."*
* 🎥 **Watch the video:** [ready2jet-one-hand-fold.mp4](../poc-higgsfield-one-hand-fold/out/ready2jet-one-hand-fold.mp4)
* 🖼️ [See the breakdown step-by-step](../poc-higgsfield-one-hand-fold/out/contact-sheet.png)

**Why it failed:** It was a disaster! The stroller didn't fold. Instead, the AI morphed it into a totally different stroller. Fake red buttons appeared, the person used *both* hands instead of one, and the camera swooped all over the place. We found out the AI server had secretly rewritten our instructions and added the camera swoop behind our backs!

### The Corrected Test (Still Failed ❌)
We turned off the AI's sneaky settings, locked the camera in place, and ran the test 3 times to be fair. 
* 🖼️ [See the breakdown of all 3 tries](../poc-higgsfield-one-hand-fold/out/corrected-three-contact-sheets.png)

**Why it failed:** 0 out of 3 videos worked. Even with perfect instructions, the AI just changed the small stroller into a bigger stroller that stayed completely open. It never folded.

**The Lesson:** The AI has watched millions of stroller videos, but it doesn't know how the hidden gears and buttons on *this specific stroller* work. Words are too vague. If you ask an AI to show a mechanical action, it will just guess—and it will usually guess wrong. For things like this, we should just show the user real, recorded videos instead of letting the AI guess!
