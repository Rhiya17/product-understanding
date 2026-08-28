const form = document.querySelector("#answer-form");
const questionInput = document.querySelector("#question");
const productSelect = document.querySelector("#product");
// MVP exception (owner decision 2026-08-27): unreviewed facts serve by
// default, labeled. TODO: revert to published-only default once the owner
// review pass promotes the catalog.
const publishedOnlyToggle = document.querySelector("#published-only");
const previewWarning = document.querySelector("#preview-warning");
const resultsRegion = document.querySelector("#results");
const emptyState = document.querySelector("#empty-state");
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

let procedureSteps = [];
let activeStepIndex = 0;

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function statusLabel(status) {
  if (status === "SUSPENDED") return "SUSPENDED — verifier alarm outstanding";
  if (status === "CANDIDATE") return "PENDING REVIEW — TODO: owner approval promotes to PUBLISHED";
  return status;
}

function readableName(value) {
  return value.replaceAll("_", " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function renderCitation(citation) {
  const wrapper = element("div", "citation");
  wrapper.append(element("blockquote", "", `“${citation.quote || "No quote recorded"}”`));
  if (citation.origin_url) {
    const link = element("a", "", `Open source · ${citation.source_id}`);
    link.href = citation.origin_url;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    wrapper.append(link);
  } else {
    wrapper.append(element("span", "meta", citation.source_id || "Source unavailable"));
  }
  return wrapper;
}

function renderMedia(media) {
  const wrapper = element("figure", "media-item");
  if (media.awaiting_approval) {
    wrapper.append(element("div", "media-approval", "MEDIA AWAITING OWNER APPROVAL"));
  }

  if (media.kind === "IMAGE") {
    const image = element("img", "bound-image");
    image.src = media.url;
    image.alt = media.rationale;
    image.loading = "lazy";
    wrapper.append(image);
  } else if (media.kind === "VIDEO_FILE") {
    const video = element("video", "bound-video");
    video.src = media.url;
    video.controls = true;
    video.preload = "metadata";
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
  wrapper.append(element("figcaption", "", media.rationale));
  return wrapper;
}

function renderResult(result, renderedMedia) {
  const unpublished = result.status !== "PUBLISHED";
  const card = element("article", `result-card${unpublished ? " unpublished" : ""}`);
  const topLine = element("div", "card-topline");
  topLine.append(element("span", `badge ${result.status}`, statusLabel(result.status)));
  topLine.append(element("span", "product-name", result.product));
  card.append(topLine);
  card.append(element("h2", "predicate", result.predicate.replaceAll("_", " ")));
  card.append(element("p", "answer", result.answer));
  card.append(element("p", "meta", `Tier ${result.tier} · ${result.claim_id}`));

  if (result.steps && result.steps.length) {
    const stepsBox = element("ol", "procedure-steps");
    result.steps.forEach((step) => {
      const item = element("li", "procedure-step-line", step.action || "");
      if (step.status !== "PUBLISHED") {
        item.append(element("span", `badge inline ${step.status}`, "pending review"));
      }
      const quote = (step.citations || [])[0];
      if (quote && quote.quote) {
        item.append(element("div", "step-quote", `“${quote.quote}” — ${quote.source_id}`));
      }
      stepsBox.append(item);
    });
    card.append(stepsBox);
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
    mediaSection.append(element("h3", "", "Official media"));
    unseenMedia.forEach((media) => mediaSection.append(renderMedia(media)));
    card.append(mediaSection);
  }
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

async function loadProducts() {
  try {
    const response = await fetch("/api/products");
    const payload = await response.json();
    payload.products.forEach((product) => {
      const option = element("option", "", `${product.brand} ${product.model}`);
      option.value = product.dir;
      productSelect.append(option);
    });
  } catch {
    errorBox.textContent = "Could not load the product catalog.";
    errorBox.hidden = false;
  }
}

async function loadProcedures() {
  procedureRegion.hidden = true;
  procedureSteps = [];
  activeStepIndex = 0;
  procedureSelect.replaceChildren();
  const placeholder = element("option", "", productSelect.value
    ? "Choose a procedure"
    : "Choose a product first");
  placeholder.value = "";
  procedureSelect.append(placeholder);
  procedureSelect.disabled = true;
  showProcedureButton.disabled = true;
  if (!productSelect.value) return;

  const query = new URLSearchParams({
    product: productSelect.value,
    preview: publishedOnlyToggle.checked ? "0" : "1",
  });
  try {
    const response = await fetch(`/api/procedures?${query}`);
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || "Could not load procedures.");
    payload.procedures.forEach((procedure) => {
      const suffix = procedure.fully_published ? "" : " · not fully published";
      const option = element("option", "", `${readableName(procedure.name)}${suffix}`);
      option.value = procedure.name;
      procedureSelect.append(option);
    });
    if (payload.procedures.length) {
      procedureSelect.disabled = false;
    } else {
      placeholder.textContent = publishedOnlyToggle.checked
        ? "No published procedures — untick 'Published facts only'"
        : "No procedures available";
    }
  } catch (error) {
    errorBox.textContent = error.message;
    errorBox.hidden = false;
  }
}

function renderProcedureStep() {
  const step = procedureSteps[activeStepIndex];
  stepStatus.className = `badge ${step.status}`;
  stepStatus.textContent = statusLabel(step.status);
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
  const query = new URLSearchParams({
    product: productSelect.value,
    procedure: procedureSelect.value,
    preview: publishedOnlyToggle.checked ? "0" : "1",
  });
  try {
    const response = await fetch(`/api/procedure?${query}`);
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || "Could not load procedure.");
    if (!payload.steps.length) throw new Error("No published steps are available for this procedure.");
    procedureSteps = payload.steps;
    activeStepIndex = 0;
    procedureTitle.textContent = readableName(payload.procedure);
    procedureBanner.hidden = payload.fully_published;
    procedureRegion.hidden = false;
    renderProcedureStep();
    procedureRegion.scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (error) {
    errorBox.textContent = error.message;
    errorBox.hidden = false;
  }
}

async function submitQuestion(event) {
  event.preventDefault();
  errorBox.hidden = true;
  notServedBox.hidden = true;
  resultsRegion.replaceChildren();
  emptyState.hidden = true;
  submitButton.disabled = true;
  submitButton.textContent = "Searching…";

  const query = new URLSearchParams({
    q: questionInput.value,
    preview: publishedOnlyToggle.checked ? "0" : "1",
    product: productSelect.value,
    top: "10",
  });

  try {
    const response = await fetch(`/api/answer?${query}`);
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || "The answer request failed.");
    if (!payload.results.length) {
      emptyState.textContent = !publishedOnlyToggle.checked
        ? "No matching published or preview facts found."
        : "No published answer found.";
      emptyState.hidden = false;
    } else {
      const renderedMedia = new Set();
      payload.results.forEach((result) => resultsRegion.append(renderResult(result, renderedMedia)));
    }
    renderNotServed(payload.not_served, !publishedOnlyToggle.checked);
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
productSelect.addEventListener("change", loadProcedures);
procedureSelect.addEventListener("change", () => {
  showProcedureButton.disabled = !procedureSelect.value;
});
showProcedureButton.addEventListener("click", showProcedure);
previousStepButton.addEventListener("click", () => {
  if (activeStepIndex > 0) {
    activeStepIndex -= 1;
    renderProcedureStep();
  }
});
nextStepButton.addEventListener("click", () => {
  if (activeStepIndex < procedureSteps.length - 1) {
    activeStepIndex += 1;
    renderProcedureStep();
  }
});
form.addEventListener("submit", submitQuestion);
loadProducts();
