# RLDX-1 Research: Why It Does Not Fit Our Video Project

*Written 2026-08-05. This was a research review, not a hands-on test. We read
the RLDX-1 model page, code, and report, but did not run the model.*

## Why we looked at RLDX-1

Our project makes short videos that explain how products work. One example is
a video showing the correct way to fold a stroller.

We need help with two jobs:

1. **Make the motion correctly.** The AI must show how the real product moves.
2. **Catch mistakes.** An automatic checker should reject a bad video before a
   person reviews it.

RLDX-1 is built to control careful robot-hand movements. Since folding a
stroller also needs careful hand movements, we asked whether RLDX-1 could help
with either job.

## Short answer

**RLDX-1 does not fit our project.** It controls a robot. It does not make
videos or check videos for mistakes. It also needs a robot or robot simulator,
and its model license does not allow commercial use.

The research still gave us a useful lead. RLDX-1 uses an image-understanding
model called **Qwen3-VL**. We later tested a larger Qwen3-VL model as a video
checker, and its first result was promising.

## What RLDX-1 does

RLDX-1 is an AI model from the robotics company RLWRLD. It was released in May
2026. Think of it as part of the brain for a robot hand.

### How an instruction becomes robot movement

The instruction comes from a person or the software running the robot. Qwen3-VL
does not create the instruction.

For example, a person or app may give RLDX-1 this goal:

> Pick up the red cup.

Then this happens:

1. **The person or app gives the instruction:** “Pick up the red cup.”
2. **The robot cameras capture the scene:** A table with a red cup, plate, and
   spoon.
3. **Qwen3-VL reads the instruction and camera images together:** It understands
   which object is the red cup and what “pick up” means.
4. **RLDX-1's action model plans the movement:** Move the arm forward, open the
   fingers, grip the cup, and lift it.
5. **The robot motors perform the movement.**
6. **The cameras capture the new position.** RLDX-1 checks the updated scene and
   decides the next movement. This loop continues until the task is complete.

In short, the instruction says **what to do**, Qwen3-VL connects that instruction
to **what the camera shows**, and RLDX-1 decides **how the robot should move**.
Its output is robot movement commands—not a picture, video, or review.

## Why it does not fit

| Our project needs | RLDX-1 provides | Result |
|---|---|---|
| A finished video | Commands for robot motors | It cannot make the video |
| A review of a video | Commands for robot motors | It cannot find video errors |
| Software that uses photos and manuals | A model connected to a robot or simulator | It does not fit our system |
| Software we can ship | A research-only model | Its license blocks commercial use |

These are basic differences. A better prompt would not fix them.

## Why the workarounds do not help

- **Use a robot simulator:** We would first need an exact 3D stroller with the
  correct hinges and moving parts. Once we build that, we can animate the fold
  directly. RLDX-1 would add extra work. This is Option 3 in the
  [video-generation alternatives](./video-generation-alternatives.md).
- **Teach a real robot:** A person would need to control the robot and show it
  the correct fold. Recording that demonstration would already give us a real
  fold video.

## The useful lead: Qwen3-VL

RLDX-1 is made from several parts. Its “eyes”—the part that understands camera
images—use the 8B version of **Qwen3-VL**.

This led us to test a larger model from the same family,
**Qwen3-VL-235B**, as our video checker. Qwen3-VL can look at pictures and
answer questions without a robot. Its Apache 2.0 license also allows commercial
use.

That matches our second job. We can turn a video into snapshots, give Qwen3-VL
those snapshots and the official product instructions, and ask it to find
mistakes.

## What happened in the first test

We tested Qwen3-VL on a Seedance video that showed a stroller folding the wrong
way. Human reviewers knew the video's problems, but we did not tell the model
what they were.

Qwen3-VL matched the human review on all six checks. It caught the wrong folding
direction, which Claude Sonnet 4.5 missed in the same test.

This is promising, but it is not proof that Qwen3-VL is ready. We tested only
one bad video and ran each check once. The full setup, results, and limits are
in the [AI Video Verifier POC](./vlm-verifier-poc-findings.md).

## Decision

1. **Stop evaluating RLDX-1 for this project.** It cannot make or check our
   videos, and we cannot use its model commercially.
2. **Continue testing Qwen3-VL as a video checker.** Test it several times with
   both correct and incorrect videos.
3. **Keep watching models that understand physical motion.** These are often
   called “world models.” NVIDIA Cosmos may be relevant because it can create
   and inspect video, but it needs a separate review of quality, cost, and
   license terms.

## Sources

- [RLDX-1 model page](https://huggingface.co/RLWRLD/RLDX-1-PT)
- [RLDX-1 code](https://github.com/RLWRLD/RLDX-1)
- [RLDX-1 technical report](https://arxiv.org/html/2605.03269v1)
- [RLDX-1 announcement](https://www.therobotreport.com/rlwrld-releases-rldx-1-a-dexterity-first-foundation-model-for-robot-hands/)
- [Qwen3-VL-235B model page](https://huggingface.co/Qwen/Qwen3-VL-235B-A22B-Instruct)
- [NVIDIA Cosmos code and overview](https://github.com/NVIDIA/Cosmos)
