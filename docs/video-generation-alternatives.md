# Making Real Product Videos: Our Options

*Written 2026-07-30. A look at the different ways to solve our video generation problem, using simple language.*

---

## Our Main Goal

**If we have the instruction manual and official photos of a stroller, can we make a video showing exactly how it folds—the real buttons, real levers, and real movement—without the AI making things up?**

In our tests, the AI we used (Higgsfield) couldn't do this. It never showed the actual folding process and even changed what the stroller looked like. This document answers: **Is there any tool out there that can actually do this right?**

---

## First, The Honest Truth: All AI Has This Problem

Before we compare tools, we need to understand something important. Our failure wasn't just bad luck. In tests run by experts, the best AI scored only 29.5 out of 100 on understanding how physical things work. They are especially bad at understanding hard parts and hinges, which is exactly how a stroller folds.

So, the question isn't "Which AI knows how strollers work?" **None of them do.** The real question is: **How do we give the AI the right information so it doesn't have to guess?**

We already found a clue: giving the AI text doesn't help much, but **giving it real pictures works like magic**. When we gave it a picture of the beginning and end, the AI did much better. The best ideas below build on this clue—giving the AI more pictures and rules, so it has less freedom to make mistakes.

---

## Quick Answers About Specific Tools

- **"cdance"** → The real name is **Seedance**, made by the company behind TikTok. It looks like one of our best options (more below).
- **"Reactor"** → This is a real company that makes instant, interactive video game worlds. It's not what we need right now for making accurate product videos.
- **Runway** → Talked about below (Options 1 and 4).
- **NVIDIA** → Talked about below (Options 2 and 3). Their tools are the closest match to our idea of "give the AI the facts first."

---

## The Four Real Ways to Solve This (Plus One Bad Idea)

Think of this like a ladder. Going down the ladder gives the AI **less room to mess up**, but means we have to do more work.

```text
More AI freedom, less work          Option 1: Use more real photos (keyframes)
        |                           Option 2: Make the AI trace a skeleton we build
        |                           Option 3: Build a 3D digital model and record it
        |                           Option 4: Edit a real video of the product folding
        v                           Option 5: Draw arrows to tell the AI how things move
Less AI freedom, more work          (Bad idea: Just hoping a newer AI is smarter)
```

---

## Option 1: Pin the Video Down with MORE Real Photos

**The idea:** Instead of just giving the AI the first and last picture, what if we gave it a picture of every step from the instruction manual? Then the AI only has to guess the tiny moments between the pictures, which makes it harder to mess up.

**Who can do this:**
Tools like **Seedance 2.0**, **Kling 3.0**, and **Vidu** let us do this. Seedance 2.0 is great because it lets us give the AI starting and ending photos, extra pictures of the product, AND a real video of a similar fold to use as a guide.

**The catch:** The AI still has to guess the parts between the pictures. Also, manuals often show close-ups from different angles, which might confuse the AI. We need to test this to see how well it handles those changes.

**Verdict:** This is the cheapest and fastest thing to try first.

---

## Option 2: Make the AI Trace a Skeleton

**The idea:** Instead of just giving the AI pictures, we can give it every single frame. We can build a simple 3D animation (like gray boxes and tubes) that shows the correct movement. Then we tell the AI: *"Paint a realistic stroller over this skeleton."* The AI only handles the colors and lighting; we control the movement.

**Who can do this:**
Tools like **Wan VACE** and **NVIDIA Cosmos Transfer** are built for this.

**The catch:** Someone has to build that 3D skeleton animation first. That takes a few days of work.

**Verdict:** This is our strongest choice for using AI. The AI doesn't have to understand how the stroller works; it just traces our work.

---

## Option 3: Build a 3D Model (No AI Guessing)

**The idea:** Skip the AI's guesswork completely. We can build a fully detailed 3D model of the stroller, animate the exact way it folds, and create a video from that. Companies have done this for years. The folding motion **cannot** be wrong because we built it perfectly.

**How we'd get the 3D model:**
The best way is to ask the manufacturer for their original design files (CAD files). If we can't get those, a 3D artist would have to recreate it by looking at photos, which takes a lot of time.

**The catch:** It takes a lot of effort and time to do this for a lot of different products. 

**Verdict:** This is the only way to guarantee it's 100% correct. It's great for our most important products.

---

## Option 4: Edit a Real Video

**The idea:** The easiest way to get the correct movement is to not generate it at all. We can film a real stroller folding with a phone. Then, we use AI to change the colors, swap the background, or make it look like a slightly different model.

**Who can do this:**
Tools like **Runway Aleph 2.0** and **Kling Multi-Elements**.

**The catch:** The AI might have a hard time editing the stroller without accidentally messing up the person's hands in the video. The hands are often covering important parts like the buttons.

**Verdict:** This is a great backup plan, especially if we already have a real video of the product.

---

## Option 5: Draw Arrows (Interactive World Models)

**The idea:** We can upload a picture of the open stroller and draw arrows to show the AI how things should move (like, "drag this handle down"). Some new models let you interact with the image almost like a video game.

**Who can do this:**
Tools like **Kling's Motion Brush** or **Genie 3**.

**The catch:** These models are mostly meant for simpler things. For a complicated stroller, the AI often makes it look like it's stretching like a rubber band instead of folding properly.

**Verdict:** A cool idea, but not quite ready for our complicated strollers yet.

---

## The Bad Idea: Just Try a Newer Text-to-Video AI

We checked all the newest, smartest AI models. None of them can do this job just by reading a text description. The models are not good at understanding how physical objects move, and relying on them just gives us videos that look pretty but are completely wrong.

---

## What We Should Do Next

We should run three cheap tests at the same time:

1. **Test A (Option 1):** Use tools like Seedance and Kling. Give them the pictures from the manual and see if they can fill in the gaps correctly.
2. **Test B (Option 2):** Build a simple 3D animation of the fold and have the AI paint over it.
3. **Test C (Option 4):** Film a real fold with someone's hands in the shot, and test if the AI can edit the stroller without messing up the fingers.

**No matter what wins, we should also:**
- Use **Option 3 (building a 3D model)** for our most important products so we always have a perfect version.
- Use a basic AI to quickly check for obvious mistakes in videos (like the stroller turning into something else), but always have a human do the final check to make sure it's perfect.

---

## Summary

Right now, AI doesn't understand how a stroller folds. Instead of trying to teach it, we need to guide it. The best ways to do this are by using more photos from the manual, giving it a 3D skeleton to trace, building our own 3D model, editing a real video, or drawing arrows to show movement. We can test all of these ideas quickly and cheaply to find out what works best.
