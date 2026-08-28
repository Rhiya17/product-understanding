const form = document.querySelector("#answer-form");
const questionInput = document.querySelector("#question");
const productSelect = document.querySelector("#product");
// MVP exception (owner decision 2026-08-27): unreviewed facts serve by
// default, labeled. TODO: revert after the owner review pass.
const publishedOnlyToggle = document.querySelector("#published-only");
const reviewModeToggle = document.querySelector("#review-mode");
const logMissesToggle = document.querySelector("#log-misses");
const previewWarning = document.querySelector("#preview-warning");
const reviewModeNote = document.querySelector("#review-mode-note");
const resultsRegion = document.querySelector("#results");
const emptyState = document.querySelector("#empty-state");
const emptyMessage = document.querySelector("#empty-message");
const exampleQuestions = document.querySelector("#example-questions");
const clarifyBox = document.querySelector("#clarify");
const errorBox = document.querySelector("#error");
const notServedBox = document.querySelector("#not-served");
const submitButton = form.querySelector("button[type='submit']");
const procedureSelect = document.querySelector("#procedure");
const showProcedureButton = document.querySelector("#show-procedure");
const procedureRegion = document.querySelector("#procedure-region");
const procedureTitle = document.querySelector("#procedure-title");
const procedureProgress = document.querySelector("#procedure-progress");
const procedureBanner = document.querySelector("#procedure-banner");
const stepStatus = document.querySelector("#step-status");
const stepNumber = document.querySelector("#step-number");
const stepAction = document.querySelector("#step-action");
const stepClaim = document.querySelector("#step-claim");
const pagePanel = document.querySelector("#page-panel");
const previousStepButton = document.querySelector("#previous-step");
const nextStepButton = document.querySelector("#next-step");

const EXAMPLES = {
  "graco-ready2jet-2212125": [
    "How do I fold the Ready2Jet stroller?",
    "What is the maximum child weight?",
    "How do I clean the stroller seat?",
  ],
  "graco-snugride-35-lite-lx": [
    "What is the max child weight for the SnugRide?",
    "How do I install the base with lower anchors?",
    "Which Graco strollers are compatible?",
  ],
  "levoit-core-300s": [
    "What does the Levoit Core 300S look like?",
    "How do I replace the filter?",
    "How quiet is it?",
  ],
  "apple-macbook-air-13-m3": [
    "What does the M3 MacBook Air look like?",
    "How do I pair a Bluetooth device?",
    "How much does it weigh?",
  ],
  default: [
    "How do I fold the Ready2Jet stroller?",
    "What is the max child weight for the SnugRide?",
    "How do I pair a Bluetooth device with the MacBook Air?",
  ],
};

let procedureSteps = [];
let activeStepIndex = 0;
let procedureStatus = null;
let currentPayload = null;
let currentQuestion = "";

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function statusLabel(status) {
  if (status === "SUSPENDED") return "Suspended";
  if (status === "CANDIDATE") return "Pending";
  return "Published";
}

function readableName(value) {
  return String(value || "").replaceAll("_", " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function renderCitation(citation) {
  const wrapper = element("div", "citation");
  wrapper.append(element("blockquote", "", `“${citation.quote || "No quote recorded"}”`));
  const sourceName = citation.source_name || "Recorded source";
  if (citation.origin_url) {
    const link = element("a", "", `Open ${sourceName} ↗`);
    link.href = citation.origin_url;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    wrapper.append(link);
  } else {
    wrapper.append(element("span", "source-name", sourceName));
  }
  return wrapper;
}

function mediaCaption(media) {
  const parts = [];
  if (media.awaiting_approval) parts.push("Pending media");
  if (media.label) parts.push(media.label);
  if (media.rationale) parts.push(media.rationale);
  if (media.provenance) parts.push(`Provenance: ${media.provenance}`);
  return parts.join(" · ");
}

function renderMedia(media) {
  const wrapper = element("figure", "media-item");
  if (media.kind === "IMAGE" || media.kind === "DERIVED_ASSET") {
    const frame = element("div", "media-frame");
    const image = element("img", "bound-image");
    image.src = media.url;
    image.alt = media.label || media.rationale;
    image.loading = "lazy";
    frame.append(image);
    if (media.watermark) frame.append(element("span", "derived-watermark", media.watermark));
    wrapper.append(frame);
  } else if (media.kind === "VIDEO_FILE") {
    const video = element("video", "bound-video");
    video.src = media.url;
    video.controls = true;
    video.preload = "metadata";
    if (media.poster_url) video.poster = media.poster_url;
    if (media.start_seconds !== null) video.currentTime = media.start_seconds;
    wrapper.append(video);
    wrapper.append(element("p", "rights-note", `Rights: ${media.rights_note}`));
  } else if (media.kind === "VIDEO_URL") {
    const link = element("a", "official-video-link", "Open official video ↗");
    const start = media.start_seconds === null ? "" : `#t=${media.start_seconds}`;
    link.href = `${media.url}${start}`;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    wrapper.append(link);
  } else if (media.kind === "PDF_PAGE") {
    const link = element("a", "manual-page-link", `Open manual page ${media.page} ↗`);
    link.href = `${media.url}#page=${media.page}`;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    wrapper.append(link);
  }
  wrapper.append(element("figcaption", "", mediaCaption(media)));
  return wrapper;
}

function renderClaimDetails(result) {
  const details = element("details", "claim-details");
  details.append(element("summary", "", "Details"));
  details.append(element("p", "meta", `Tier ${result.tier} · ${result.claim_id}`));
  if (result.raw_answer) details.append(element("p", "raw-answer", result.raw_answer));
  return details;
}

async function recordReview(productDir, claimId, disposition, rationale, controls) {
  controls.querySelectorAll("button").forEach((button) => { button.disabled = true; });
  try {
    const response = await fetch("/api/reviews", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ product: productDir, claim_id: claimId, disposition, rationale }),
    });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || "Could not record review.");
    await runSearch();
  } catch (error) {
    errorBox.textContent = error.message;
    errorBox.hidden = false;
    controls.querySelectorAll("button").forEach((button) => { button.disabled = false; });
  }
}

function reviewControls(productDir, claimId, tier) {
  const controls = element("div", "review-actions");
  controls.append(element("p", "review-scope", `${tier} · one decision recorded to this pack`));
  const rationale = element("input", "review-rationale");
  rationale.type = "text";
  rationale.maxLength = 2000;
  rationale.placeholder = "Optional rationale";
  rationale.setAttribute("aria-label", `Review rationale for ${claimId}`);
  controls.append(rationale);
  const buttons = element("div", "review-buttons");
  [
    ["Approve for publish", "APPROVED_FOR_PUBLISH", "approve"],
    ["Reject for serving", "REJECTED_FOR_SERVING", "reject"],
    ["Needs rework", "NEEDS_REWORK", "rework"],
  ].forEach(([label, disposition, className]) => {
    const button = element("button", className, label);
    button.type = "button";
    button.addEventListener("click", () => recordReview(
      productDir, claimId, disposition, rationale.value, controls));
    buttons.append(button);
  });
  controls.append(buttons);
  return controls;
}

async function reportIssue(result, note, status) {
  try {
    const response = await fetch("/api/feedback", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: currentQuestion, product: result.product_dir, claim_id: result.claim_id, note }),
    });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || "Could not save feedback.");
    status.textContent = "Saved locally.";
  } catch (error) {
    status.textContent = error.message;
  }
}

function renderFeedback(result) {
  if (result.claim_id.startsWith("procedure:")) return null;
  const details = element("details", "feedback-control");
  details.append(element("summary", "", "Report an issue"));
  const note = element("input", "feedback-note");
  note.type = "text";
  note.maxLength = 2000;
  note.placeholder = "Optional note";
  note.setAttribute("aria-label", `Issue note for ${result.claim_id}`);
  const button = element("button", "secondary-button", "Save report locally");
  button.type = "button";
  const status = element("span", "feedback-status");
  button.addEventListener("click", () => reportIssue(result, note.value, status));
  details.append(note, button, status);
  return details;
}

async function openProcedure(productDir, procedure) {
  productSelect.value = productDir;
  await loadProcedures();
  procedureSelect.value = procedure;
  showProcedureButton.disabled = false;
  await showProcedure();
}

function renderResult(result, renderedMedia) {
  const unpublished = result.status !== "PUBLISHED";
  const card = element("article", `result-card${unpublished ? " unpublished" : ""}`);
  const topLine = element("div", "card-topline");
  topLine.append(element("span", `status-chip ${result.status}`, statusLabel(result.status)));
  topLine.append(element("span", "product-name", result.product));
  card.append(topLine);

  const heading = result.type === "STEP"
    ? `Step ${result.step_number} of ${readableName(result.procedure)}`
    : (result.type === "PROCEDURE" ? readableName(result.procedure) : readableName(result.predicate));
  card.append(element("h2", "predicate", heading));
  card.append(element("p", "answer", result.display_text || result.answer));

  if (result.steps && result.steps.length) {
    const stepsBox = element("ol", "procedure-steps");
    result.steps.forEach((step) => {
      const item = element("li", "procedure-step-line", step.action || "");
      if (step.status !== result.status) {
        item.append(element("span", `status-chip inline ${step.status}`, statusLabel(step.status)));
      }
      const quote = (step.citations || [])[0];
      if (quote && quote.quote) {
        item.append(element("div", "step-quote", `“${quote.quote}” — ${quote.source_name || "Recorded source"}`));
      }
      if (reviewModeToggle.checked && step.status !== "PUBLISHED") {
        item.append(reviewControls(result.product_dir, step.claim_id, step.tier));
      }
      stepsBox.append(item);
    });
    card.append(stepsBox);
  }

  if (result.type === "STEP" && result.procedure) {
    const procedureButton = element("button", "procedure-link", "View full ordered procedure");
    procedureButton.type = "button";
    procedureButton.addEventListener("click", () => openProcedure(result.product_dir, result.procedure));
    card.append(procedureButton);
  }

  if (result.citations.length) {
    const citations = element("div", "citations");
    citations.append(element("h3", "", "Source evidence"));
    result.citations.forEach((citation) => citations.append(renderCitation(citation)));
    card.append(citations);
  }

  const unseenMedia = (result.media || []).filter((media) => {
    if (renderedMedia.has(media.id)) return false;
    renderedMedia.add(media.id);
    return true;
  });
  if (unseenMedia.length) {
    const mediaSection = element("div", "media-section");
    mediaSection.append(element("h3", "", "Evidence-linked media"));
    unseenMedia.forEach((media) => mediaSection.append(renderMedia(media)));
    card.append(mediaSection);
  }

  card.append(renderClaimDetails(result));
  if (reviewModeToggle.checked && unpublished && !result.claim_id.startsWith("procedure:")) {
    card.append(reviewControls(result.product_dir, result.claim_id, result.tier));
  }
  const feedback = renderFeedback(result);
  if (feedback) card.append(feedback);
  return card;
}

function renderNotServed(counts, preview) {
  notServedBox.hidden = true;
  const entries = Object.entries(counts).filter(([, count]) => count > 0);
  if (!preview && entries.length) {
    const detail = entries.map(([status, count]) => `${count} ${status.toLowerCase()}`).join(", ");
    notServedBox.textContent = `Not served: ${detail} matching fact${entries.length === 1 && entries[0][1] === 1 ? "" : "s"}. Untick 'Published facts only' to see them, labeled.`;
    notServedBox.hidden = false;
  }
}

function renderExamples() {
  exampleQuestions.replaceChildren();
  (EXAMPLES[productSelect.value] || EXAMPLES.default).forEach((question) => {
    const button = element("button", "example-question", question);
    button.type = "button";
    button.addEventListener("click", async () => {
      questionInput.value = question;
      await runSearch();
    });
    exampleQuestions.append(button);
  });
}

function renderClarification(clarify) {
  clarifyBox.replaceChildren(element("h2", "", clarify.prompt));
  const choices = element("div", "clarify-buttons");
  clarify.candidates.forEach((candidate) => {
    const button = element("button", "", candidate.product);
    button.type = "button";
    button.addEventListener("click", async () => {
      productSelect.value = candidate.product_dir;
      await loadProcedures();
      await runSearch();
    });
    choices.append(button);
  });
  clarifyBox.append(choices);
  clarifyBox.hidden = false;
}

function renderPayload(payload) {
  resultsRegion.replaceChildren();
  clarifyBox.hidden = true;
  emptyState.hidden = true;
  if (payload.mode === "clarify") {
    renderClarification(payload.clarify);
    return;
  }
  if (!payload.results.length) {
    if (payload.gap) {
      emptyMessage.textContent = `We don't have a verified answer for this — recorded gap: ${payload.gap.reason}`;
      emptyState.classList.add("gap-state");
    } else {
      emptyMessage.textContent = "No answers matched. Try one of these questions:";
      emptyState.classList.remove("gap-state");
    }
    renderExamples();
    emptyState.hidden = false;
  } else {
    const renderedMedia = new Set();
    payload.results.forEach((result) => resultsRegion.append(renderResult(result, renderedMedia)));
  }
  renderNotServed(payload.not_served, !publishedOnlyToggle.checked);
}

async function loadProducts() {
  try {
    const response = await fetch("/api/products");
    const payload = await response.json();
    payload.products.forEach((product) => {
      const option = element("option", "", `${product.brand} ${product.model}`);
      option.value = product.dir;
      productSelect.append(option);
    });
    renderExamples();
  } catch {
    errorBox.textContent = "Could not load the product catalog.";
    errorBox.hidden = false;
  }
}

async function loadReviewConfig() {
  try {
    const response = await fetch("/api/review-config");
    const payload = await response.json();
    reviewModeToggle.disabled = !payload.enabled;
    reviewModeToggle.title = payload.enabled ? `Reviewing as ${payload.reviewer}` : "Restart the server with --reviewer owner@example.com";
    reviewModeNote.textContent = payload.enabled
      ? `Reviewing as ${payload.reviewer}. ${payload.recording_note}`
      : "Review writing is off. Restart with --reviewer owner@example.com to record decisions.";
  } catch {
    reviewModeToggle.disabled = true;
  }
}

async function loadProcedures() {
  procedureRegion.hidden = true;
  procedureSteps = [];
  activeStepIndex = 0;
  procedureSelect.replaceChildren();
  const placeholder = element("option", "", productSelect.value ? "Choose a procedure" : "Choose a product first");
  placeholder.value = "";
  procedureSelect.append(placeholder);
  procedureSelect.disabled = true;
  showProcedureButton.disabled = true;
  if (!productSelect.value) return;

  const query = new URLSearchParams({ product: productSelect.value, preview: publishedOnlyToggle.checked ? "0" : "1" });
  try {
    const response = await fetch(`/api/procedures?${query}`);
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || "Could not load procedures.");
    payload.procedures.forEach((procedure) => {
      const suffix = procedure.publication_state === "partial" ? " · partially published" : "";
      const option = element("option", "", `${readableName(procedure.name)}${suffix}`);
      option.value = procedure.name;
      procedureSelect.append(option);
    });
    if (payload.procedures.length) {
      procedureSelect.disabled = false;
    } else {
      placeholder.textContent = publishedOnlyToggle.checked ? "No published procedures — untick 'Published facts only'" : "No procedures available";
    }
  } catch (error) {
    errorBox.textContent = error.message;
    errorBox.hidden = false;
  }
}

function renderProcedureStep() {
  const step = procedureSteps[activeStepIndex];
  stepStatus.className = `status-chip ${step.status}`;
  stepStatus.textContent = statusLabel(step.status);
  stepStatus.hidden = step.status === procedureStatus;
  stepNumber.textContent = `Step ${step.step_number}`;
  stepAction.textContent = step.action;
  stepClaim.textContent = step.claim_id;
  procedureProgress.textContent = `${activeStepIndex + 1} of ${procedureSteps.length}`;
  previousStepButton.disabled = activeStepIndex === 0;
  nextStepButton.disabled = activeStepIndex === procedureSteps.length - 1;
  pagePanel.replaceChildren();
  if (step.page_image_url) {
    const image = element("img", "manual-page");
    image.src = step.page_image_url;
    image.alt = `Authentic whole manual page for step ${step.step_number}`;
    pagePanel.append(image);
    pagePanel.append(element("figcaption", "", "Whole authentic manual page · 144 DPI · no crop or annotation"));
  } else {
    pagePanel.append(element("div", "no-page", "No approved page binding for this step. Showing verified step text only."));
  }
}

async function showProcedure() {
  if (!productSelect.value || !procedureSelect.value) return;
  errorBox.hidden = true;
  const query = new URLSearchParams({ product: productSelect.value, procedure: procedureSelect.value, preview: publishedOnlyToggle.checked ? "0" : "1" });
  try {
    const response = await fetch(`/api/procedure?${query}`);
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || "Could not load procedure.");
    if (!payload.steps.length) throw new Error("No published steps are available for this procedure.");
    procedureSteps = payload.steps;
    activeStepIndex = 0;
    const statuses = new Set(payload.steps.map((step) => step.status));
    procedureStatus = statuses.size === 1 ? payload.steps[0].status : "MIXED";
    procedureTitle.textContent = readableName(payload.procedure);
    procedureBanner.textContent = payload.fully_published ? "" : "This procedure includes pending review decisions.";
    procedureBanner.hidden = payload.fully_published;
    procedureRegion.hidden = false;
    renderProcedureStep();
    procedureRegion.scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (error) {
    errorBox.textContent = error.message;
    errorBox.hidden = false;
  }
}

async function logMiss(question) {
  try {
    await fetch("/api/feedback", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, product: productSelect.value, claim_id: null }),
    });
  } catch {
    // Logging is explicitly optional and must not obscure the honest miss.
  }
}

function enterSearchLayout() {
  const wasCompact = document.body.classList.contains("has-searched");
  const previousScroll = window.scrollY;
  document.body.classList.add("has-searched");
  requestAnimationFrame(() => window.scrollTo(0, wasCompact ? previousScroll : 0));
}

async function runSearch() {
  if (!questionInput.value.trim()) return;
  enterSearchLayout();
  errorBox.hidden = true;
  notServedBox.hidden = true;
  resultsRegion.replaceChildren();
  emptyState.hidden = true;
  clarifyBox.hidden = true;
  submitButton.disabled = true;
  submitButton.textContent = "Searching…";
  currentQuestion = questionInput.value.trim();
  const query = new URLSearchParams({ q: currentQuestion, preview: publishedOnlyToggle.checked ? "0" : "1", product: productSelect.value, top: "10" });

  try {
    const response = await fetch(`/api/answer?${query}`);
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || "The answer request failed.");
    currentPayload = payload;
    renderPayload(payload);
    if (!payload.results.length && payload.mode !== "clarify" && logMissesToggle.checked) await logMiss(currentQuestion);
  } catch (error) {
    errorBox.textContent = error.message;
    errorBox.hidden = false;
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = "Find answer";
  }
}

publishedOnlyToggle.addEventListener("change", () => {
  previewWarning.hidden = publishedOnlyToggle.checked;
  loadProcedures();
});
reviewModeToggle.addEventListener("change", () => {
  reviewModeNote.hidden = !reviewModeToggle.checked;
  if (currentPayload) renderPayload(currentPayload);
});
productSelect.addEventListener("change", () => {
  renderExamples();
  loadProcedures();
});
procedureSelect.addEventListener("change", () => { showProcedureButton.disabled = !procedureSelect.value; });
showProcedureButton.addEventListener("click", showProcedure);
previousStepButton.addEventListener("click", () => {
  if (activeStepIndex > 0) { activeStepIndex -= 1; renderProcedureStep(); }
});
nextStepButton.addEventListener("click", () => {
  if (activeStepIndex < procedureSteps.length - 1) { activeStepIndex += 1; renderProcedureStep(); }
});
form.addEventListener("submit", (event) => { event.preventDefault(); runSearch(); });
loadProducts();
loadReviewConfig();
