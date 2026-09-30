"""
Unit tests for Docker Compose hardening separation and syntax validation.
UPA-1217: Compose Hardening Override Separation.
"""

import os
from pathlib import Path
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
COMPOSE_BASE = REPO_ROOT / "docker-compose.yml"
COMPOSE_HARDENING = REPO_ROOT / "docker-compose.hardening.yml"
COMPOSE_OVERRIDE = REPO_ROOT / "docker-compose.override.yml"


def test_compose_base_parses_successfully():
    assert COMPOSE_BASE.exists(), "docker-compose.yml must exist"
    with open(COMPOSE_BASE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert isinstance(data, dict), "docker-compose.yml must be a valid YAML mapping"
    assert "services" in data, "docker-compose.yml must contain 'services'"
    assert set(data["services"].keys()) == {"redis", "api", "worker", "caddy"}


def test_compose_hardening_parses_successfully():
    assert COMPOSE_HARDENING.exists(), "docker-compose.hardening.yml must exist"
    with open(COMPOSE_HARDENING, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert isinstance(data, dict), "docker-compose.hardening.yml must be a valid YAML mapping"
    assert "services" in data, "docker-compose.hardening.yml must contain 'services'"


def test_neither_compose_file_contains_obsolete_version():
    with open(COMPOSE_BASE, "r", encoding="utf-8") as f:
        base_data = yaml.safe_load(f)
    with open(COMPOSE_HARDENING, "r", encoding="utf-8") as f:
        hardening_data = yaml.safe_load(f)

    assert "version" not in base_data, "Obsolete 'version' key must be removed from docker-compose.yml"
    assert "version" not in hardening_data, "Obsolete 'version' key must not be present in docker-compose.hardening.yml"


def test_compose_override_is_absent():
    assert not COMPOSE_OVERRIDE.exists(), (
        "docker-compose.override.yml must be removed so hardening is not auto-loaded"
    )


def test_base_compose_does_not_contain_hardening():
    with open(COMPOSE_BASE, "r", encoding="utf-8") as f:
        base_data = yaml.safe_load(f)

    services = base_data.get("services", {})
    for svc_name, svc_cfg in services.items():
        assert "cap_drop" not in svc_cfg, f"{svc_name} in base compose must not contain cap_drop"
        assert "security_opt" not in svc_cfg, f"{svc_name} in base compose must not contain security_opt"


def test_hardening_overlay_contains_required_api_settings():
    with open(COMPOSE_HARDENING, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    api_cfg = data.get("services", {}).get("api", {})
    assert api_cfg.get("cap_drop") == ["ALL"], "api must have cap_drop: [ALL]"
    assert api_cfg.get("cap_add") == ["NET_BIND_SERVICE"], "api must have cap_add: [NET_BIND_SERVICE]"
    assert api_cfg.get("security_opt") == ["no-new-privileges:true"], "api must have no-new-privileges:true"


def test_hardening_overlay_contains_required_worker_settings():
    with open(COMPOSE_HARDENING, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    worker_cfg = data.get("services", {}).get("worker", {})
    assert worker_cfg.get("cap_drop") == ["ALL"], "worker must have cap_drop: [ALL]"
    assert worker_cfg.get("security_opt") == ["no-new-privileges:true"], "worker must have no-new-privileges:true"


def test_hardening_overlay_introduces_no_unrelated_services():
    with open(COMPOSE_HARDENING, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    services = data.get("services", {})
    assert set(services.keys()) == {"api", "worker"}, "Hardening overlay must target only api and worker"


def test_merged_compose_configuration_is_valid_and_applies_hardening():
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

    assert merged_services["api"]["cap_drop"] == ["ALL"]
    assert merged_services["api"]["cap_add"] == ["NET_BIND_SERVICE"]
    assert merged_services["api"]["security_opt"] == ["no-new-privileges:true"]
    assert merged_services["worker"]["cap_drop"] == ["ALL"]
    assert merged_services["worker"]["security_opt"] == ["no-new-privileges:true"]
    assert "cap_drop" not in merged_services["redis"]
    assert "cap_drop" not in merged_services["caddy"]
