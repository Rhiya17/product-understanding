"""Offline test guard for every pytest run in this repository.

Routine tests must never call a provider, download a source or spend money.
Provider credentials are removed from the environment and any socket
connection to a non-loopback address fails. A deliberate live canary sets
SHOWME_ALLOW_NETWORK=1 and still needs an approved spend manifest.
"""

import ipaddress
import os
import socket

import pytest

PROVIDER_ENV_VARS = ("FAL_KEY", "FAL_API_KEY", "OPENAI_API_KEY",
                     "ANTHROPIC_API_KEY")


def _is_loopback(address):
    host = address[0] if isinstance(address, tuple) else address
    if host in ("localhost", ""):
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


@pytest.fixture(autouse=True)
def _offline(monkeypatch):
    if os.environ.get("SHOWME_ALLOW_NETWORK") == "1":
        yield
        return
    for name in PROVIDER_ENV_VARS:
        monkeypatch.delenv(name, raising=False)
    original_connect = socket.socket.connect

    def guarded_connect(sock, address):
        if sock.family == socket.AF_UNIX or _is_loopback(address):
            return original_connect(sock, address)
        raise RuntimeError(f"offline test attempted network access to {address}")

    monkeypatch.setattr(socket.socket, "connect", guarded_connect)
    yield


@pytest.fixture(autouse=True)
def _isolated_video_store(monkeypatch, tmp_path):
    """Saved video requests and renders go to a per-test directory."""
    monkeypatch.setenv("SHOWME_DATA_DIR", str(tmp_path / "showme-data"))
    monkeypatch.delenv("SHOWME_DEV_MEDIA", raising=False)
    monkeypatch.delenv("SHOWME_SERVE_RESEARCH_MEDIA", raising=False)
