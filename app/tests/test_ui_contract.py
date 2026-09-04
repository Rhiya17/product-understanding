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


def test_published_only_is_the_default_and_stale_pending_banner_is_hidden():
    html = source("index.html")
    assert 'id="published-only" name="published-only" type="checkbox" checked' in html
    assert 'id="preview-warning" class="preview-warning" hidden' in html
    assert "PENDING REVIEW" not in html


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


def test_generated_procedure_video_is_rendered_as_an_autoplaying_video():
    javascript = source("app.js")
    html = source("index.html")
    assert 'media.asset_type === "PROCEDURE_VIDEO_MP4"' in javascript
    assert "video.autoplay = true" in javascript
    assert 'video.addEventListener("canplay"' in javascript
    assert "video.poster = media.poster_url" in javascript
    assert '"Generated walkthrough"' in javascript
    assert "resultsForDisplay(payload)" in javascript
    assert 'result.type === "PROCEDURE"' in javascript
    assert 'result.procedure === "connect_wired_or_bluetooth_device"' in javascript
    assert "Generated walkthroughs are labeled" in html


def test_luna_primary_media_leads_the_dedicated_media_panel():
    javascript = source("app.js")
    css = source("styles.css")
    assert "function mediaModality(media)" in javascript
    assert "presentation.primary_modality" in javascript
    assert 'element("div", "card-media")' in javascript
    assert 'element("div", "card-body")' in javascript
    assert "columns.append(mediaPanel, textPanel)" in javascript
    assert "orderedMedia" in javascript
    assert "renderResult(result, renderedMedia, payload.presentation)" in javascript
    assert ".card-columns" in css


def test_video_placeholder_polls_and_swaps_in_the_generated_walkthrough():
    javascript = source("app.js")
    css = source("styles.css")
    assert "result.video_job" in javascript
    assert "renderVideoSlot(result.video_job)" in javascript
    assert "pollVideoJob" in javascript
    assert "job.poll_url" in javascript
    assert 'payload.state === "ready" && payload.media' in javascript
    assert "slot.replaceChildren(renderMedia(payload.media))" in javascript
    assert "stopVideoPolls()" in javascript
    assert "Video generating…" in javascript
    assert ".video-slot" in css
    assert "prefers-reduced-motion" in css


def test_internal_fields_are_inside_collapsed_details_and_lead_is_bold():
    javascript = source("app.js")
    css = source("styles.css")
    assert 'element("details", "claim-details")' in javascript
    assert "Tier ${result.tier} · ${result.claim_id}" in javascript
    assert ".answer { font-size: 1.1rem; font-weight: 750;" in css
