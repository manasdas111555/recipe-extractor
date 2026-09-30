"""
Unit tests for Production API port shielding and documentation exposure control.
UPA-1226: Production API Public Exposure & Port Shielding.
"""

from pathlib import Path
import yaml
from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.app.core.config import Settings

REPO_ROOT = Path(__file__).resolve().parent.parent
COMPOSE_BASE = REPO_ROOT / "docker-compose.yml"
COMPOSE_HARDENING = REPO_ROOT / "docker-compose.hardening.yml"
CADDYFILE = REPO_ROOT / "Caddyfile"


def test_docker_compose_api_port_bound_strictly_to_loopback():
    """Asserts that docker-compose.yml binds FastAPI port 8000 exclusively to 127.0.0.1 (UPA-1226)."""
    assert COMPOSE_BASE.exists(), "docker-compose.yml must exist"
    with open(COMPOSE_BASE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    api_ports = data.get("services", {}).get("api", {}).get("ports", [])
    assert api_ports == ["127.0.0.1:8000:8000"], (
        f"API service must bind strictly to 127.0.0.1:8000:8000 to prevent public internet exposure, got: {api_ports}"
    )
    assert "8000:8000" not in api_ports, "Public 0.0.0.0:8000 port binding must not exist"
    assert "0.0.0.0:8000:8000" not in api_ports, "Explicit 0.0.0.0:8000 binding must not exist"


def test_docker_compose_redis_port_bound_strictly_to_loopback():
    """Asserts that docker-compose.yml binds Redis port 6379 strictly to loopback."""
    with open(COMPOSE_BASE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    redis_ports = data.get("services", {}).get("redis", {}).get("ports", [])
    assert redis_ports == ["127.0.0.1:6379:6379"], (
        f"Redis service must bind strictly to 127.0.0.1:6379:6379, got: {redis_ports}"
    )


def test_caddyfile_reverse_proxy_targets_internal_docker_network():
    """Asserts that Caddy reverse proxy forwards traffic to internal container api:8000."""
    assert CADDYFILE.exists(), "Caddyfile must exist"
    with open(CADDYFILE, "r", encoding="utf-8") as f:
        content = f.read()

    assert "reverse_proxy api:8000" in content, (
        "Caddy must forward to 'api:8000' over the internal Docker network"
    )


def test_fastapi_docs_configurable_in_settings():
    """Asserts that Settings allows configuring or disabling DOCS_URL, REDOC_URL, and OPENAPI_URL."""
    # Test explicit custom routes
    s_custom = Settings(
        ENVIRONMENT="test",
        DOCS_URL="/custom-docs",
        REDOC_URL="/custom-redoc",
        OPENAPI_URL="/custom-openapi.json"
    )
    assert s_custom.DOCS_URL == "/custom-docs"
    assert s_custom.REDOC_URL == "/custom-redoc"
    assert s_custom.OPENAPI_URL == "/custom-openapi.json"

    # Test normalization of empty/null strings to None
    s_disabled = Settings(
        ENVIRONMENT="test",
        DOCS_URL="",
        REDOC_URL="none",
        OPENAPI_URL="null"
    )
    assert s_disabled.DOCS_URL is None
    assert s_disabled.REDOC_URL is None
    assert s_disabled.OPENAPI_URL is None


def test_fastapi_endpoints_return_404_when_docs_disabled():
    """Asserts that when docs settings are None, FastAPI returns HTTP 404 on /docs, /redoc, and /openapi.json."""
    app_disabled = FastAPI(
        title="Test App Disabled Docs",
        docs_url=None,
        redoc_url=None,
        openapi_url=None
    )

    @app_disabled.get("/health")
    def health():
        return {"status": "ok"}

    client = TestClient(app_disabled)
    assert client.get("/docs").status_code == 404
    assert client.get("/redoc").status_code == 404
    assert client.get("/openapi.json").status_code == 404
    assert client.get("/health").status_code == 200


def test_fastapi_endpoints_available_in_development_default():
    """Asserts that in standard development mode, /docs and /openapi.json are accessible."""
    app_dev = FastAPI(
        title="Test App Dev Docs",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )

    client = TestClient(app_dev)
    assert client.get("/docs").status_code == 200
    assert client.get("/openapi.json").status_code == 200


def test_merged_compose_hardening_overlay_validity():
    """Asserts that the merged compose stack applies loopback port binding and hardening overlay cleanly."""
    with open(COMPOSE_BASE, "r", encoding="utf-8") as f:
        base = yaml.safe_load(f)
    with open(COMPOSE_HARDENING, "r", encoding="utf-8") as f:
        hardening = yaml.safe_load(f)

    merged_services = {}
    for svc, cfg in base.get("services", {}).items():
        merged_services[svc] = dict(cfg)

    for svc, cfg in hardening.get("services", {}).items():
        if svc in merged_services:
            merged_services[svc].update(cfg)

    # Verify loopback port binding is preserved under merged overlay
    assert merged_services["api"]["ports"] == ["127.0.0.1:8000:8000"]
    assert merged_services["redis"]["ports"] == ["127.0.0.1:6379:6379"]
    # Verify security hardening options remain active
    assert merged_services["api"]["cap_drop"] == ["ALL"]
    assert merged_services["api"]["cap_add"] == ["NET_BIND_SERVICE"]
    assert merged_services["api"]["security_opt"] == ["no-new-privileges:true"]
