from pathlib import Path


STATIC = Path(__file__).resolve().parents[1] / "static"


def source(name):
    return (STATIC / name).read_text(encoding="utf-8")


def test_search_first_compact_state_keeps_search_and_answers_in_normal_flow():
    html = source("index.html")
    css = source("styles.css")
    javascript = source("app.js")
    assert 'id="answer-form"' in html
    assert ".has-searched .hero-copy" in css
    assert ".has-searched .answer-region { margin-top: 1rem; }" in css
    assert 'document.body.classList.add("has-searched")' in javascript
    assert "wasCompact ? previousScroll : 0" in javascript


def test_pending_labels_are_quiet_and_step_chips_only_show_when_different():
    javascript = source("app.js")
    css = source("styles.css")
    assert 'return "Pending"' in javascript
    assert "step.status !== result.status" in javascript
    assert "Pending media" in javascript
    assert ".status-chip::before" in css
    assert "MEDIA AWAITING OWNER APPROVAL" not in javascript


def test_landing_examples_and_click_to_search_are_wired():
    html = source("index.html")
    javascript = source("app.js")
    assert 'id="example-questions"' in html
    assert "EXAMPLES" in javascript
    assert "questionInput.value = question" in javascript
    assert "await runSearch()" in javascript


def test_review_feedback_derived_and_clarification_controls_are_present():
    html = source("index.html")
    javascript = source("app.js")
    assert 'id="review-mode"' in html
    assert 'fetch("/api/reviews"' in javascript
    assert 'fetch("/api/feedback"' in javascript
    assert 'media.kind === "DERIVED_ASSET"' in javascript
    assert "derived-watermark" in javascript
    assert "renderClarification" in javascript


def test_internal_fields_are_inside_collapsed_details_and_lead_is_bold():
    javascript = source("app.js")
    css = source("styles.css")
    assert 'element("details", "claim-details")' in javascript
    assert "Tier ${result.tier} · ${result.claim_id}" in javascript
    assert ".answer { font-size: 1.1rem; font-weight: 750;" in css
