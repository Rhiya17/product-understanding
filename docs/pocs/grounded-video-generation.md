# Grounded Video Generation for Product Understanding

## Introduction
The core goal of the Interactive Video Product Understanding engine is: **"How to generate video for a product grounded in reality."** The system must produce videos that answer user questions factually and visually, adhering strictly to precise mechanical constraints, product dimensions, and correct visual states.

## POC Experiment Summary
We conducted two Proof of Concept (POC) experiments using the Higgsfield API to evaluate the current capability of generative AI models for deterministic, fact-based video generation.

1. **Geometry POC ([poc-higgsfield-geometry](./poc-higgsfield-geometry))**
   *   **Goal:** Evaluate if Higgsfield can accurately visualize computed geometry (e.g., "Will this stroller fit in the trunk of my Tesla Model Y?").
   *   **Findings:** Unconstrained prompt-based generation fails to retain geometric truth; the model hallucinates dimensions. However, utilizing a "first-last-frame" interpolation approach successfully managed to pin the geometry correctly at the endpoints, reducing spatial drift.

2. **Mechanical Interaction POC ([poc-higgsfield-one-hand-fold](./poc-higgsfield-one-hand-fold))**
   *   **Goal:** Test if Higgsfield can generate accurate, procedural product interactions (e.g., a one-hand fold instruction for a Graco Ready2Jet stroller) without inventing parts or changing the product's shape.
   *   **Findings:** The model struggled significantly with physical mechanics. It changed the physical structure of the stroller, used both hands instead of one, and introduced unintended camera motions unless parameters were heavily locked down. Prompt-only generative AI is currently inadequate for exact product-operation instructions.

## Deep Dive: Approaches to Grounded Video Generation
To successfully generate a fact-based video that respects reality, we must explore alternative approaches beyond basic text-to-video prompting. 

To evaluate these approaches, we use two simple guiding questions:
*   **Question A (Mechanical):** *"Show me how to fold the Graco Ready2Jet stroller."* (Exact make and precise folding instructions are known, but the video must be generated factually).
*   **Question B (Spatial):** *"Will this stroller fit in the trunk of my Tesla Model Y?"*

### Approach 1: First/Last Frame Interpolation APIs
**How it works:** Instead of prompting a model to "generate a stroller folding," we supply two verified, deterministic images: Image 1 (an open stroller) and Image 2 (a folded stroller). The AI model (e.g., Wan-2.1 or Kling AI's start/end frame API) is strictly tasked with synthesizing the visual transition between them.
*   **Pros:** Prevents hallucination of the end-state. The Geometry POC demonstrated that this approach successfully pinned geometry for trunk placement.
*   **Cons:** While the endpoints are locked, the model may still invent physically impossible transitions *between* the two frames (e.g., a mechanical joint morphing like liquid instead of rotating on an axis).
*   **Application:** Best suited for **Question B**, where we provide an image of an empty trunk and an image of the stroller inside the trunk. It is risky for **Question A**, as the folding motion itself is the instruction.

### Approach 2: Node-Based Constraints (e.g., ComfyUI with ControlNet)
**How it works:** A custom generative pipeline where the AI is constrained frame-by-frame by structural data, such as Depth maps, Canny edges, or Pose estimation. 
*   **Pros:** Offers extremely high control. For Question B, a basic 3D bounding box can be programmatically generated and used as a ControlNet depth map. This forces the generative model to paint the stroller *exactly* within mathematically verified dimensions.
*   **Cons:** High engineering overhead. Creating the necessary structural masks for complex, multi-joint mechanical movements (Question A) is difficult without already having a full 3D animation.
*   **Application:** Excellent for **Question B** (Spatial Geometry), where bounding boxes and spatial masks are easily computed programmatically.

### Approach 3: Hybrid 3D Simulation + AI Stylization
**How it works:** The action is not "generated" by AI at all. Instead, a lightweight headless 3D engine (e.g., Unity, WebGL, or a deterministic fit engine) calculates and renders a crude, deterministic 3D block-out of the action. Generative AI (Image-to-Video via ControlNet) is only used to stylize this crude animation into a photorealistic visual.
*   **Pros:** 100% physically and geometrically accurate. Completely solves the hallucination problem because the joint rotation is calculated by a physics engine, not predicted by diffusion.
*   **Cons:** Requires maintaining 3D assets, CAD models, or basic rigs for the products.
*   **Application:** The most robust and defensible solution for **Question A** (Mechanical Operation) and **Question B**. It guarantees that the visual matches the precise folding instructions.

### Approach 4: Segment Retrieval and Compositing
**How it works:** Do not generate motion. Instead, retrieve an existing verified video segment of the exact stroller folding. Use AI only for compositing (e.g., highlighting the specific button to press, or overlaying the retrieved stroller clip over a photo of the user's car).
*   **Pros:** Mathematically zero risk of mechanical hallucination. The fastest and cheapest to execute.
*   **Cons:** Fails if no video of that specific angle or action exists in the database.
*   **Application:** Should always be the primary fallback for **Question A** before attempting to generate new frames.

## Conclusion and Next Steps
Pure generative AI models are optimized for visual plausibility, not mechanical truth. To ground our product in reality, our architecture must prioritize **Approach 4 (Retrieval)**. When generation is required, we must use **Approach 3 (Hybrid 3D)** for mechanical operations (Question A) and **Approach 2 (Node-Based Constraints)** for static spatial placements (Question B). Prompt-only generation should be deprecated for exact operations.
