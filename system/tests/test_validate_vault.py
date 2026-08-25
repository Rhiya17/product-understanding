import hashlib
import importlib.util
import json
from pathlib import Path

from pypdf import PdfWriter


REPO_ROOT = Path(__file__).resolve().parents[2]
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_vault.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_vault_test", VALIDATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_vault(tmp_path, local_path="source.md", content=b"Official source text."):
    vault = tmp_path / "source-vault"
    product = vault / "test-product"
    product.mkdir(parents=True)
    (vault / "catalog.json").write_text(json.dumps({
        "products": [{"dir": "test-product"}],
    }), encoding="utf-8")
    source = product / local_path
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_bytes(content)
    manifest = {
        "identity": {"product_id": "test-product"},
        "sources": [{
            "source_id": "src_one",
            "local_path": local_path,
            "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        }],
    }
    (product / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    return vault, product


def test_orphan_file_hard_fails(tmp_path, capsys):
    vault, product = make_vault(tmp_path)
    (product / "unregistered.txt").write_text("orphan", encoding="utf-8")
    validator = load_validator()
    validator.VAULT = vault

    assert validator.main() == 1
    output = capsys.readouterr().out
    assert "orphan file not listed in manifest: unregistered.txt" in output


def test_image_only_pdf_hard_fails(tmp_path, capsys):
    vault, product = make_vault(tmp_path)
    source = product / "source.md"
    source.unlink()
    pdf = product / "manuals" / "blank.pdf"
    pdf.parent.mkdir()
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    with pdf.open("wb") as handle:
        writer.write(handle)
    manifest = json.loads((product / "manifest.json").read_text())
    manifest["sources"][0]["local_path"] = "manuals/blank.pdf"
    manifest["sources"][0]["sha256"] = hashlib.sha256(pdf.read_bytes()).hexdigest()
    (product / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    validator = load_validator()
    validator.VAULT = vault

    assert validator.main() == 1
    output = capsys.readouterr().out
    assert "PDF has no extractable text in the first 10 pages" in output


def test_declared_text_file_passes(tmp_path, capsys):
    vault, _product = make_vault(tmp_path)
    validator = load_validator()
    validator.VAULT = vault

    assert validator.main() == 0
    assert "vault OK" in capsys.readouterr().out
