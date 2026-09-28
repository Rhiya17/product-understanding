import json
import pytest
import os
from pathlib import Path
from app import keyframe_synthesis

class MockFalClient:
    def __init__(self, verdicts):
        self.verdicts = iter(verdicts)
        self.uploads = []
    def upload_file(self, path):
        self.uploads.append(path)
        return "https://mock.com/" + Path(path).name
    def submit(self, endpoint, arguments):
        class Handle:
            def __init__(self, endpoint, verdicts_iter):
                self.endpoint = endpoint
                self.verdicts_iter = verdicts_iter
                self.request_id = "req_123"
            def get(self):
                if "any-llm/vision" in self.endpoint:
                    try:
                        v = next(self.verdicts_iter)
                    except StopIteration:
                        v = {"verdict": "pass"}
                    return {"output": "```json\n" + json.dumps(v) + "\n```"}
                return {"images": [{"url": "https://mock.com/img.png"}]}
        return Handle(endpoint, self.verdicts)

@pytest.fixture(autouse=True)
def offline_downloads(monkeypatch):
    """Serve generated-image downloads locally; the mock URLs are not real."""
    import io

    def fake_urlopen(url, timeout=None):
        return io.BytesIO(b"\x89PNG\r\n\x1a\n fake image bytes for " + url.encode())

    monkeypatch.setattr(keyframe_synthesis.urllib.request, "urlopen", fake_urlopen)


def make_env(tmp_path):
    packs = tmp_path / "packs"
    vault = tmp_path / "source-vault"
    packs.mkdir()
    vault.mkdir()
    pack_dir = packs / "acme"
    vault_dir = vault / "acme"
    pack_dir.mkdir()
    vault_dir.mkdir()
    (pack_dir / "claims.json").write_text("[]", encoding="utf-8")
    (pack_dir / "media-bindings.json").write_text("{}", encoding="utf-8")
    (vault_dir / "manifest.json").write_text("{}", encoding="utf-8")
    return packs

def test_synthesis_pass_path(tmp_path):
    packs = make_env(tmp_path)
    client = MockFalClient([{"verdict": "pass"}])
    state = {"state_id": "s1", "description": "test state"}
    out = keyframe_synthesis.synthesize_and_verify_state(state, "proc1", packs, "acme", client)
    assert out.is_file()
    assert out.with_name(f"{out.name}.provenance.json").is_file()

def test_synthesis_retry_then_pass(tmp_path):
    packs = make_env(tmp_path)
    client = MockFalClient([{"verdict": "fail", "verdict_reason": "bad"}, {"verdict": "pass"}])
    state = {"state_id": "s1", "description": "test state"}
    out = keyframe_synthesis.synthesize_and_verify_state(state, "proc1", packs, "acme", client)
    assert out.is_file()

def test_synthesis_retry_then_fail(tmp_path):
    packs = make_env(tmp_path)
    client = MockFalClient([{"verdict": "fail", "verdict_reason": "bad"}, {"verdict": "fail", "verdict_reason": "bad"}])
    state = {"state_id": "s1", "description": "test state"}
    with pytest.raises(RuntimeError, match="failed verification twice"):
        keyframe_synthesis.synthesize_and_verify_state(state, "proc1", packs, "acme", client)
    out = tmp_path / "generated-assets" / "acme" / "keyframes" / "proc1-s1.png"
    assert not out.exists()

def test_cache_rules(tmp_path):
    packs = make_env(tmp_path)
    client = MockFalClient([{"verdict": "pass"}])
    state = {"state_id": "s1"}
    
    # Generate once
    out = keyframe_synthesis.synthesize_and_verify_state(state, "proc1", packs, "acme", client)
    
    # Mess up provenance to simulate mock
    prov_path = out.with_name(f"{out.name}.provenance.json")
    prov_data = json.loads(prov_path.read_text())
    prov_data["request_id"] = "mock_req_123"
    prov_path.write_text(json.dumps(prov_data))
    
    # Generate again - should bypass cache because of "mock" in request_id
    out2 = keyframe_synthesis.synthesize_and_verify_state(state, "proc1", packs, "acme", client)
    prov_data2 = json.loads(prov_path.read_text())
    assert prov_data2["request_id"] == "req_123"

def test_ladder_order(tmp_path):
    packs = make_env(tmp_path)
    client = MockFalClient([{"verdict": "pass"}])
    vault_dir = tmp_path / "source-vault" / "acme"
    (vault_dir / "manifest.json").write_text(json.dumps({
        "sources": [{"source_id": "src_1", "local_path": "img.png"}]
    }))
    (vault_dir / "img.png").write_text("test")
    
    # 1. curated_path
    state = {"state_id": "s1", "curated_path": "source-vault/acme/img.png"}
    out = keyframe_synthesis.resolve_state(state, "proc1", packs, "acme", client, None)
    assert out == tmp_path / "source-vault" / "acme" / "img.png"
    
    # 2. evidence_source_id
    state = {"state_id": "s1", "evidence_source_id": "src_1"}
    out = keyframe_synthesis.resolve_state(state, "proc1", packs, "acme", client, None)
    assert out.name == "img.png"
    prov_path = tmp_path / "generated-assets" / "acme" / "keyframes" / "proc1-s1.png.provenance.json"
    assert json.loads(prov_path.read_text())["retrieved_from"] == "src_1"
