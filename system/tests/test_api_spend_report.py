from scripts.report_api_spend import reconcile, summarize


def test_video_and_ledger_are_counted_once_and_reservations_are_separate():
    video = [dict(id='sp_a', at='2026-10-07T22:00:00+00:00', job_id='job_a', label='openai/model', amount=.4),
             dict(id='sp_b', at='2026-10-07T23:00:00+00:00', job_id='job_b', label='anthropic/model', amount=1)]
    events = [dict(event='reserve', category='video_generation', job_id='job_a', label='openai/model',
                   at=video[0]['at'], worst_case_usd=2),
              dict(event='reserve', category='video_generation', reservation_id='sp_b', worst_case_usd=1),
              dict(event='settle', reservation_id='sp_a', actual_usd=.4),
              dict(event='settle', reservation_id='sp_b', actual_usd=None)]
    rows = reconcile(video, events, {})
    assert len(rows) == 2
    total = summarize(rows)
    assert total['settled_estimated_usd'] == .4
    assert total['unreconciled_reservation_usd'] == 1


def test_external_verifier_and_zero_cost_rejection_are_not_lost():
    events = [dict(event='reserve', reservation_id='res_a', run_id='verify', worst_case_usd=.1),
              dict(event='settle', reservation_id='res_a', actual_usd=.002),
              dict(event='reserve', reservation_id='res_b', run_id='verify', worst_case_usd=.1),
              dict(event='settle', reservation_id='res_b', actual_usd=0)]
    total = summarize(reconcile([], events, {'verify': {'provider': 'fal.ai', 'model': 'qwen'}}))
    assert total['settled_estimated_usd'] == .002
    assert total['unreconciled_reservation_usd'] == 0
    assert total['providers']['fal.ai']['settled_calls'] == 2
