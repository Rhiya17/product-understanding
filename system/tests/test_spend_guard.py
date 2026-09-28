import pytest

from system import spend_guard
from system.spend_guard import SpendGuard, SpendRefused


def make_manifest(**overrides):
    manifest = {
        "run_id": "run_answer_eval_1",
        "category": "answer_verifier",
        "purpose": "launch verifier evaluation",
        "provider": "fake",
        "model": "fake-model",
        "inputs": {"claims": "sha256:abc"},
        "max_calls": 3,
        "cap_usd": 2.0,
        "retry_policy": "no automatic retry",
    }
    manifest.update(overrides)
    return manifest


@pytest.fixture
def guard(tmp_path):
    return SpendGuard(tmp_path / "approvals.jsonl", tmp_path / "ledger.jsonl")


def approve(guard, manifest):
    return spend_guard.record_owner_approval(
        manifest, "owner@example.com", approvals_path=guard.approvals_path)


def test_credentials_or_ceilings_alone_never_start_a_run(guard, monkeypatch):
    monkeypatch.setenv("FAL_KEY", "configured-looking-credential")
    with pytest.raises(SpendRefused, match="no owner approval"):
        guard.authorize(make_manifest(), "appr_missing")


def test_changed_manifest_needs_fresh_approval(guard):
    receipt = approve(guard, make_manifest())
    for change in ({"provider": "other"}, {"model": "bigger"},
                   {"inputs": {"claims": "sha256:def"}}, {"max_calls": 9}):
        with pytest.raises(SpendRefused, match="fresh approval"):
            guard.authorize(make_manifest(**change), receipt["approval_id"])


def test_run_cap_is_enforced_before_the_call(guard):
    receipt = approve(guard, make_manifest(cap_usd=1.0))
    run = guard.authorize(make_manifest(cap_usd=1.0), receipt["approval_id"])
    reservation = run.reserve(0.6, "call 1")
    run.settle(reservation, 0.5, "ok")
    with pytest.raises(SpendRefused, match="exceeds remaining"):
        run.reserve(0.6, "over-cap retry")


def test_category_and_total_ceilings_win_over_run_cap(guard):
    first = make_manifest(run_id="a", cap_usd=5.0)
    run = guard.authorize(first, approve(guard, first)["approval_id"])
    run.settle(run.reserve(4.5, "call"), 4.5, "ok")
    run.finish("done")
    second = make_manifest(run_id="b", cap_usd=5.0)
    run = guard.authorize(second, approve(guard, second)["approval_id"])
    assert run.remaining_usd() == pytest.approx(0.5)
    with pytest.raises(SpendRefused):
        run.reserve(1.0, "category exhausted")


def test_cap_above_work_order_ceiling_is_rejected(guard):
    with pytest.raises(SpendRefused, match="outside"):
        approve(guard, make_manifest(category="astra_authoring", cap_usd=20))


def test_unknown_billing_stops_further_paid_work(guard):
    manifest = make_manifest()
    receipt = approve(guard, manifest)
    run = guard.authorize(manifest, receipt["approval_id"])
    run.settle(run.reserve(0.5, "uncertain submit"), None, "timeout")
    with pytest.raises(SpendRefused, match="run stopped"):
        run.reserve(0.1, "retry")
    with pytest.raises(SpendRefused, match="unknown billing"):
        guard.authorize(manifest, receipt["approval_id"])


def test_rerun_after_finish_needs_new_approval(guard):
    manifest = make_manifest()
    receipt = approve(guard, manifest)
    run = guard.authorize(manifest, receipt["approval_id"])
    run.settle(run.reserve(0.5, "call"), 0.2, "ok")
    run.finish("partial")
    with pytest.raises(SpendRefused, match="already used"):
        guard.authorize(manifest, receipt["approval_id"])


def test_call_limit_and_revocation(guard):
    manifest = make_manifest(max_calls=1)
    receipt = approve(guard, manifest)
    run = guard.authorize(manifest, receipt["approval_id"])
    run.settle(run.reserve(0.1, "only call"), 0.1, "ok")
    with pytest.raises(SpendRefused, match="call limit"):
        run.reserve(0.1, "second call")
    spend_guard.revoke_approval(receipt["approval_id"], "owner@example.com",
                                approvals_path=guard.approvals_path)
    with pytest.raises(SpendRefused, match="revoked"):
        guard.authorize(manifest, receipt["approval_id"])


def test_ledger_never_rewrites_the_manifest(guard):
    manifest = make_manifest()
    before = spend_guard.manifest_digest(manifest)
    receipt = approve(guard, manifest)
    run = guard.authorize(manifest, receipt["approval_id"])
    run.settle(run.reserve(0.5, "call"), 0.4, "ok")
    assert spend_guard.manifest_digest(manifest) == before
    assert receipt["manifest_digest"] == before
