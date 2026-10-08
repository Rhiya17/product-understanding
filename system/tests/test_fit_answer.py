"""Integration checks of the cargo-fit answer against the real evidence packs."""

from system.answer_engine import AnswerEngine


def fit_doc(question="Can i fit Ready2jet stroller in tesla model y trunk", product=None):
    return AnswerEngine().answer(question, product).to_dict()


def test_fit_question_routes_to_the_fit_answer():
    doc = fit_doc()
    assert doc["coverage"]["procedure_id"] == "fit_tesla_model_y_trunk"
    assert doc["product"]["product_dir"] == "graco-ready2jet-2212125"
    assert doc["context"]["secondary_product"] == "tesla-model-y"


def test_fit_is_never_called_confirmed_without_a_verified_floor_width():
    doc = fit_doc("Will the Ready2Jet stroller fit in my Tesla Model Y trunk?",
                  "graco-ready2jet-2212125")
    verdict = doc["coverage"]["fit"]["verdict"]
    assert verdict in {"FITS_CONFIRMED", "LIKELY_FITS_UNCONFIRMED", "DOES_NOT_FIT", "UNKNOWN"}
    if verdict != "FITS_CONFIRMED":
        assert not doc["direct_answer"].startswith("Yes.")
        assert doc["status"] != "ready"
    if verdict == "LIKELY_FITS_UNCONFIRMED":
        assert "floor_width" in doc["gap"]["unknown_constraints"]


def test_every_cited_measurement_is_servable():
    engine = AnswerEngine()
    doc = engine.answer("Can i fit Ready2jet stroller in tesla model y trunk").to_dict()
    products = engine.products()
    for source in doc["sources"]:
        owner = next(p for p in products.values() if source["claim_id"] in p.claims)
        assert owner.eligible(source["claim_id"]), source["claim_id"]


def test_plain_stroller_questions_do_not_route_to_fit():
    doc = fit_doc("How do I fold the Ready2Jet stroller?")
    assert doc["coverage"].get("procedure_id") != "fit_tesla_model_y_trunk"
