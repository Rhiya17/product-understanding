const form = document.querySelector("#answer-form");
const questionInput = document.querySelector("#question");
const productSelect = document.querySelector("#product");
const previewToggle = document.querySelector("#preview");
const previewWarning = document.querySelector("#preview-warning");
const resultsRegion = document.querySelector("#results");
const emptyState = document.querySelector("#empty-state");
const errorBox = document.querySelector("#error");
const notServedBox = document.querySelector("#not-served");
const submitButton = form.querySelector("button[type='submit']");

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function statusLabel(status) {
  if (status === "SUSPENDED") return "SUSPENDED — verifier alarm outstanding";
  if (status === "CANDIDATE") return "CANDIDATE — not human-reviewed";
  return status;
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

function renderResult(result) {
  const unpublished = result.status !== "PUBLISHED";
  const card = element("article", `result-card${unpublished ? " unpublished" : ""}`);
  const topLine = element("div", "card-topline");
  topLine.append(element("span", `badge ${result.status}`, statusLabel(result.status)));
  topLine.append(element("span", "product-name", result.product));
  card.append(topLine);
  card.append(element("h2", "predicate", result.predicate.replaceAll("_", " ")));
  card.append(element("p", "answer", result.answer));
  card.append(element("p", "meta", `Tier ${result.tier} · ${result.claim_id}`));

  if (result.citations.length) {
    const citations = element("div", "citations");
    citations.append(element("h3", "", "Source evidence"));
    result.citations.forEach((citation) => citations.append(renderCitation(citation)));
    card.append(citations);
  }
  return card;
}

function renderNotServed(counts, preview) {
  notServedBox.hidden = true;
  const entries = Object.entries(counts).filter(([, count]) => count > 0);
  if (!preview && entries.length) {
    const detail = entries.map(([status, count]) => `${count} ${status.toLowerCase()}`).join(", ");
    notServedBox.textContent = `Not served: ${detail} matching fact${entries.length === 1 && entries[0][1] === 1 ? "" : "s"}. Turn on Internal preview to inspect candidate or suspended facts.`;
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
    preview: previewToggle.checked ? "1" : "0",
    product: productSelect.value,
    top: "10",
  });

  try {
    const response = await fetch(`/api/answer?${query}`);
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || "The answer request failed.");
    if (!payload.results.length) {
      emptyState.textContent = previewToggle.checked
        ? "No matching published or preview facts found."
        : "No published answer found.";
      emptyState.hidden = false;
    } else {
      payload.results.forEach((result) => resultsRegion.append(renderResult(result)));
    }
    renderNotServed(payload.not_served, previewToggle.checked);
  } catch (error) {
    errorBox.textContent = error.message;
    errorBox.hidden = false;
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = "Find answer";
  }
}

previewToggle.addEventListener("change", () => {
  previewWarning.hidden = !previewToggle.checked;
});
form.addEventListener("submit", submitQuestion);
loadProducts();
