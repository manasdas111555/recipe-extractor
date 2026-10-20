"""
Test Suite: E2E Evidence Artifact Isolation & Non-Destructive Framework (UPA-1403)
==================================================================================
Tests verify_evidence_manifest in scripts/verify_promotion.py to guarantee:
1. Custom manifest paths passed via manifest_path argument are verified accurately.
2. Auto-detection of EVIDENCE_MANIFEST_PATH environment variable.
3. Auto-detection of EVIDENCE_OUTPUT_DIR and EVIDENCE_MANIFEST_FILENAME environment variables.
4. Fallback to default path when environment variables are unset.
5. Invariant preservation: strict live classification and commit SHA checks hold under all custom paths.
"""

import json
import os
from pathlib import Path
import pytest
from scripts.verify_promotion import verify_evidence_manifest, ROOT_DIR

SAMPLE_COMMIT_SHA = "332d766439d01832439303c417f0666c9356acc8"


def create_sample_manifest(
    classification: str = "live",
    overall_status: str = "PASS",
    commit_sha: str = SAMPLE_COMMIT_SHA,
    passed: int = 1,
    failed: int = 0,
    blocked: int = 0,
    not_run: int = 0,
    environment: str = "staging",
) -> dict:
    return {
        "schemaVersion": 1,
        "runId": "isolated_test_run_001",
        "commitSha": commit_sha,
        "environment": environment,
        "startTime": "2026-10-20T12:00:00.000Z",
        "endTime": "2026-10-20T12:00:05.000Z",
        "totalDurationMs": 5000,
        "overallStatus": overall_status,
        "executionClassification": classification,
        "summary": {
            "total": passed + failed + blocked + not_run,
            "passed": passed,
            "failed": failed,
            "blocked": blocked,
            "notRun": not_run,
        },
        "tests": [
            {
                "testId": "smoke_staging_hero",
                "title": "Smoke Staging Hero Test",
                "outcome": overall_status,
                "executionType": classification if classification in ["mocked", "live"] else "mocked",
                "evidencePaths": {
                    "screenshots": ["screenshot.png"],
                    "video": "video.webm",
                    "trace": "trace.zip",
                },
                "assertionOutcomes": [{"name": "assertion_1", "status": "PASS"}],
                "capturedConsoleErrors": [],
                "capturedHttpFailures": [],
            }
        ],
    }


def test_verify_manifest_via_explicit_path_argument(tmp_path: Path):
    manifest_path = tmp_path / "custom-evidence-manifest.json"
    manifest_data = create_sample_manifest()
    manifest_path.write_text(json.dumps(manifest_data), encoding="utf-8")

    result = verify_evidence_manifest("staging", manifest_path=manifest_path, expected_sha=SAMPLE_COMMIT_SHA)
    assert result is True


def test_verify_manifest_via_evidence_manifest_path_env(tmp_path: Path, monkeypatch):
    manifest_path = tmp_path / "env-evidence-manifest.json"
    manifest_data = create_sample_manifest()
    manifest_path.write_text(json.dumps(manifest_data), encoding="utf-8")

    monkeypatch.setenv("EVIDENCE_MANIFEST_PATH", str(manifest_path))

    result = verify_evidence_manifest("staging", manifest_path=None, expected_sha=SAMPLE_COMMIT_SHA)
    assert result is True


def test_verify_manifest_via_evidence_output_dir_env(tmp_path: Path, monkeypatch):
    custom_dir = tmp_path / "isolated-staging-smoke"
    custom_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = custom_dir / "evidence-manifest.json"
    manifest_data = create_sample_manifest()
    manifest_path.write_text(json.dumps(manifest_data), encoding="utf-8")

    monkeypatch.delenv("EVIDENCE_MANIFEST_PATH", raising=False)
    monkeypatch.setenv("EVIDENCE_OUTPUT_DIR", str(custom_dir))

    result = verify_evidence_manifest("staging", manifest_path=None, expected_sha=SAMPLE_COMMIT_SHA)
    assert result is True


def test_verify_manifest_via_output_dir_and_custom_filename(tmp_path: Path, monkeypatch):
    custom_dir = tmp_path / "isolated-staging-smoke"
    custom_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = custom_dir / "smoke-run-manifest.json"
    manifest_data = create_sample_manifest()
    manifest_path.write_text(json.dumps(manifest_data), encoding="utf-8")

    monkeypatch.delenv("EVIDENCE_MANIFEST_PATH", raising=False)
    monkeypatch.setenv("EVIDENCE_OUTPUT_DIR", str(custom_dir))
    monkeypatch.setenv("EVIDENCE_MANIFEST_FILENAME", "smoke-run-manifest.json")

    result = verify_evidence_manifest("staging", manifest_path=None, expected_sha=SAMPLE_COMMIT_SHA)
    assert result is True


def test_verify_manifest_missing_file_fails_closed(tmp_path: Path, monkeypatch):
    non_existent = tmp_path / "does_not_exist"
    monkeypatch.delenv("EVIDENCE_MANIFEST_PATH", raising=False)
    monkeypatch.setenv("EVIDENCE_OUTPUT_DIR", str(non_existent))

    result = verify_evidence_manifest("staging", manifest_path=None, expected_sha=SAMPLE_COMMIT_SHA)
    assert result is False


def test_verify_manifest_invariants_preserved_under_custom_path(tmp_path: Path):
    # Mocked classification must be strictly rejected for staging
    mocked_path = tmp_path / "mocked-manifest.json"
    mocked_data = create_sample_manifest(classification="mocked")
    mocked_path.write_text(json.dumps(mocked_data), encoding="utf-8")

    result_mocked = verify_evidence_manifest("staging", manifest_path=mocked_path, expected_sha=SAMPLE_COMMIT_SHA)
    assert result_mocked is False

    # SHA mismatch must be strictly rejected for staging
    sha_mismatch_path = tmp_path / "sha-mismatch-manifest.json"
    sha_data = create_sample_manifest(commit_sha="wrong_sha_12345678901234567890123456789012")
    sha_mismatch_path.write_text(json.dumps(sha_data), encoding="utf-8")

    result_sha = verify_evidence_manifest("staging", manifest_path=sha_mismatch_path, expected_sha=SAMPLE_COMMIT_SHA)
    assert result_sha is False
