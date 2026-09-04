"""Background generation and pack registration of procedure walkthrough videos.

When a question resolves to a documented procedure that has no bound video,
the server enqueues a job here and answers immediately with text and images.
A daemon thread renders the walkthrough with the deterministic local
generator, then registers the asset and its claim binding into the product's
evidence pack — unapproved, so it serves as labeled pending media until the
owner reviews it.
"""

import datetime
import hashlib
import json
import os
import re
import sys
import tempfile
import threading
from pathlib import Path


def _deterministic_generator(product_label, procedure, steps, output, poster,
                             reference_image=None, product_dir=None):
    """Offline typographic fallback; used only when fal.ai is unavailable."""
    scripts_dir = Path(__file__).resolve().parents[1] / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    from generate_procedure_walkthrough import generate
    generate(product_label, procedure, steps, output, poster)
    return {
        "provider": "local deterministic Pillow/OpenCV procedure renderer",
        "generator": "scripts/generate_procedure_walkthrough.py",
        "license_status": "INTERNAL_GENERATED_DEMO",
        "rights_note": (
            "Generated typographic walkthrough; every word comes from the "
            "extracted step claims. No manufacturer imagery is embedded."),
        "external_spend_usd": 0,
    }


def fal_credentials_present():
    return bool(os.environ.get("FAL_KEY") or os.environ.get("FAL_API_KEY"))


def renderer_mode():
    """The active video renderer.

    "keyframe" (the default, also spelled "auto") is the grounded pipeline:
    it only generates for procedures with registered keyframes and refuses
    everything else. "fal" (direct wan generation) and "deterministic"
    (typographic slides) are explicit opt-ins kept for experiments and
    offline development.
    """
    renderer = os.environ.get("SHOWME_VIDEO_RENDERER", "auto").lower()
    return renderer if renderer in {"fal", "deterministic", "keyframe"} \
        else "keyframe"


def _sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _atomic_write_json(path, document):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
                "w", encoding="utf-8", dir=path.parent,
                prefix=f".{path.name}.", suffix=".tmp",
                delete=False) as temporary:
            temporary_path = Path(temporary.name)
            json.dump(document, temporary, ensure_ascii=False, indent=2)
            temporary.write("\n")
            temporary.flush()
            os.fsync(temporary.fileno())
        os.replace(temporary_path, path)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


class VideoJobManager:
    """Deduplicated per-(product, procedure) walkthrough generation jobs."""

    def __init__(self, packs_root, output_root=None, generator=None,
                 vault_root=None):
        self.packs_root = Path(packs_root).resolve()
        self.vault_root = Path(vault_root).resolve() if vault_root else None
        self.output_root = Path(
            output_root or self.packs_root.parent / "generated-assets"
        ).resolve()
        self._generator = generator
        self._jobs = {}
        self._lock = threading.Lock()
        self._pack_lock = threading.Lock()

    @staticmethod
    def _slug(value):
        return re.sub(r"[^a-z0-9]+", "-", str(value).lower()).strip("-")

    def job_id_for(self, product_dir, procedure):
        digest = hashlib.sha256(
            f"{product_dir}::{procedure}".encode()).hexdigest()[:16]
        return f"vidjob_{digest}"

    def ensure(self, product_dir, product_label, procedure, steps):
        """Return the job for this procedure, starting generation once."""
        job_id = self.job_id_for(product_dir, procedure)
        with self._lock:
            job = self._jobs.get(job_id)
            if job is None:
                job = {
                    "job_id": job_id,
                    "state": "queued",
                    "product_dir": product_dir,
                    "procedure": procedure,
                    "claim_ids": [step.get("claim_id") for step in steps
                                  if step.get("claim_id")],
                    "asset_id": None,
                    "binding_id": None,
                }
                self._jobs[job_id] = job
                threading.Thread(
                    target=self._run,
                    args=(job, product_label, [dict(step) for step in steps]),
                    daemon=True).start()
            return dict(job)

    def status(self, job_id):
        with self._lock:
            job = self._jobs.get(job_id)
            return dict(job) if job else None

    def can_generate(self, product_dir, procedure):
        """Whether the active renderer could produce a video for this job.

        The grounded default refuses procedures with no registered keyframes,
        so the server attaches no placeholder for them at all.
        """
        if self._generator is not None:
            return True
        if renderer_mode() in {"fal", "deterministic"}:
            return True
        from app import keyframe_video
        return keyframe_video.registry_entry(
            self.packs_root, product_dir, procedure) is not None

    def _resolve_generator(self):
        if self._generator is not None:
            return self._generator
        mode = renderer_mode()
        if mode == "fal":
            from app import fal_video
            return fal_video.generate
        if mode == "deterministic":
            return _deterministic_generator
        from app import keyframe_video
        return keyframe_video.make_generator(self.packs_root)

    def _set(self, job, **fields):
        with self._lock:
            job.update(fields)

    def _run(self, job, product_label, steps):
        self._set(job, state="running")
        try:
            slug = self._slug(job["procedure"])
            out_dir = self.output_root / job["product_dir"]
            output = out_dir / f"{slug}-walkthrough.mp4"
            poster = out_dir / f"{slug}-walkthrough-poster.png"
            metadata = self._resolve_generator()(
                product_label, job["procedure"], steps, output, poster,
                reference_image=self._reference_image(job),
                product_dir=job["product_dir"])
            asset_id, binding_id = self._register(
                job, output, poster, metadata)
            self._set(job, state="ready", asset_id=asset_id,
                      binding_id=binding_id)
        except Exception as error:  # Details stay in the server log.
            sys.stderr.write(
                f"video job {job['job_id']} failed: {error!r}\n")
            self._set(job, state="failed")

    def _reference_image(self, job):
        """Local path of an evidence image bound to this procedure's claims."""
        if self.vault_root is None:
            return None
        pack_dir = self.packs_root / job["product_dir"]
        try:
            bindings = json.loads(
                (pack_dir / "media-bindings.json").read_text(
                    encoding="utf-8")).get("bindings", [])
            manifest = json.loads(
                (self.vault_root / job["product_dir"] / "manifest.json")
                .read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
        sources = {source.get("source_id"): source
                   for source in manifest.get("sources", [])
                   if isinstance(source, dict)}
        wanted = set(job["claim_ids"])
        for binding in bindings:
            if (not isinstance(binding, dict)
                    or binding.get("kind") != "IMAGE"
                    or not wanted & set(binding.get("claim_ids", []))):
                continue
            source = sources.get(binding.get("source_id")) or {}
            local_path = source.get("local_path")
            if not local_path:
                continue
            product_root = (self.vault_root / job["product_dir"]).resolve()
            candidate = (product_root / local_path).resolve()
            if product_root in candidate.parents and candidate.is_file():
                return candidate
        return None

    def _relative_to_repo(self, path):
        relative = Path(os.path.relpath(path, self.packs_root.parent))
        if ".." in relative.parts:
            raise ValueError(
                "Generated asset must live under the packs root's parent")
        return relative.as_posix()

    _METADATA_FIELDS = (
        "provider", "generator", "license_status", "rights_note",
        "external_spend_usd", "request_id", "generation_prompt",
        "reference_image", "verification_local_path", "keyframe_provenance",
    )

    def _register(self, job, output, poster, metadata=None):
        procedure = job["procedure"]
        safe = re.sub(r"[^a-z0-9]+", "_", procedure.lower()).strip("_")
        asset_id = f"derived_generated_{safe}_walkthrough"
        binding_id = f"mb_generated_{safe}_walkthrough"
        now = datetime.datetime.now(datetime.timezone.utc)
        readable = procedure.replace("_", " ").strip()
        asset = {
            "asset_id": asset_id,
            "type": "PROCEDURE_VIDEO_MP4",
            "label": f"Generated {readable} walkthrough",
            "watermark": "INTERNAL ONLY — GENERATED WALKTHROUGH",
            "local_path": self._relative_to_repo(output),
            "sha256": _sha256_file(output),
            "poster_local_path": self._relative_to_repo(poster),
            "poster_sha256": _sha256_file(poster),
            "created_at": now.isoformat().replace("+00:00", "Z"),
            "provider": "local deterministic Pillow/OpenCV procedure renderer",
            "source_claim_ids": list(job["claim_ids"]),
            "generator": "scripts/generate_procedure_walkthrough.py",
            "license_status": "INTERNAL_GENERATED_DEMO",
            "rights_note": (
                "Generated typographic walkthrough; every word comes from the "
                "extracted step claims. No manufacturer imagery is embedded."),
            "approved_by": None,
            "internal_only": True,
            "provisional_unverified": True,
            "external_spend_usd": 0,
        }
        for field in self._METADATA_FIELDS:
            if isinstance(metadata, dict) and field in metadata:
                asset[field] = metadata[field]
        binding = {
            "binding_id": binding_id,
            "claim_ids": list(job["claim_ids"]),
            "source_id": asset_id,
            "kind": "DERIVED_ASSET",
            "page": None,
            "start_seconds": None,
            "end_seconds": None,
            "rationale": (
                f"Generated walkthrough visualizes the documented "
                f"{readable} steps in order; pending owner review."),
            "proposed_by": "agent",
            "approved_by": None,
        }
        pack_dir = self.packs_root / job["product_dir"]
        with self._pack_lock:
            self._upsert(pack_dir / "derived-assets.json", "assets",
                         "asset_id", asset)
            self._upsert(pack_dir / "media-bindings.json", "bindings",
                         "binding_id", binding)
        return asset_id, binding_id

    @staticmethod
    def _upsert(path, list_key, id_key, record):
        try:
            document = json.loads(Path(path).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            document = {}
        if not isinstance(document, dict):
            document = {}
        entries = [entry for entry in document.get(list_key, [])
                   if isinstance(entry, dict)
                   and entry.get(id_key) != record[id_key]]
        entries.append(record)
        document[list_key] = entries
        _atomic_write_json(path, document)
