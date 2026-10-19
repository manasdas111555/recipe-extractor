"""
Test Suite: Release Gate Evidence Manifest Verification (UPA-1401 P0)
======================================================================
Tests verify_evidence_manifest in scripts/verify_promotion.py to guarantee:
1. Valid mocked manifests are accepted for dev environment.
2. Mocked manifests are strictly rejected for staging and prod release gates.
3. Missing or invalid classifications fail closed.
4. Valid live-classified manifests with matching SHA and passing counters are accepted.
5. Existing SHA-mismatch, missing-file, and anti-false-green protections remain intact.
"""

import json
from pathlib import Path
import pytest
from scripts.verify_promotion import verify_evidence_manifest

SAMPLE_COMMIT_SHA = "92ad7b0212e551eb64345c2ceea4b6ab66498d4d"


def create_manifest(
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
        "runId": "test_run_123",
        "commitSha": commit_sha,
        "environment": environment,
        "startTime": "2026-10-19T00:00:00.000Z",
        "endTime": "2026-10-19T00:00:05.000Z",
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
                "testId": "test_case_1",
                "title": "sample test case",
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
                "sanitized": True,
            }
        ],
    }


def test_mocked_manifest_valid_for_dev(tmp_path: Path):
    manifest = create_manifest(classification="mocked", environment="dev")
    manifest_path = tmp_path / "evidence-manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    result = verify_evidence_manifest(
        target_env="dev",
        manifest_path=manifest_path,
        expected_sha=SAMPLE_COMMIT_SHA,
    )
    assert result is True


def test_mocked_manifest_rejected_for_staging_gate(tmp_path: Path):
    manifest = create_manifest(classification="mocked", environment="staging")
    manifest_path = tmp_path / "evidence-manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    result = verify_evidence_manifest(
        target_env="staging",
        manifest_path=manifest_path,
        expected_sha=SAMPLE_COMMIT_SHA,
    )
    assert result is False


def test_mocked_manifest_rejected_for_prod_gate(tmp_path: Path):
    manifest = create_manifest(classification="mocked", environment="staging")
    manifest_path = tmp_path / "evidence-manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    result = verify_evidence_manifest(
        target_env="prod",
        manifest_path=manifest_path,
        expected_sha=SAMPLE_COMMIT_SHA,
    )
    assert result is False


def test_missing_classification_fails_closed(tmp_path: Path):
    manifest = create_manifest(classification="")
    del manifest["executionClassification"]
    manifest_path = tmp_path / "evidence-manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    result = verify_evidence_manifest(
        target_env="staging",
        manifest_path=manifest_path,
        expected_sha=SAMPLE_COMMIT_SHA,
    )
    assert result is False


def test_invalid_classification_fails_closed(tmp_path: Path):
    manifest = create_manifest(classification="synthetic")
    manifest_path = tmp_path / "evidence-manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    result = verify_evidence_manifest(
        target_env="staging",
        manifest_path=manifest_path,
        expected_sha=SAMPLE_COMMIT_SHA,
    )
    assert result is False


def test_valid_live_manifest_accepted_for_staging(tmp_path: Path):
    manifest = create_manifest(classification="live", environment="staging")
    manifest_path = tmp_path / "evidence-manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    result = verify_evidence_manifest(
        target_env="staging",
        manifest_path=manifest_path,
        expected_sha=SAMPLE_COMMIT_SHA,
    )
    assert result is True


def test_valid_live_manifest_accepted_for_prod(tmp_path: Path):
    manifest = create_manifest(classification="live", environment="staging")
    manifest_path = tmp_path / "evidence-manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    result = verify_evidence_manifest(
        target_env="prod",
        manifest_path=manifest_path,
        expected_sha=SAMPLE_COMMIT_SHA,
    )
    assert result is True


def test_commit_sha_mismatch_fails_closed(tmp_path: Path):
    manifest = create_manifest(classification="live", commit_sha=SAMPLE_COMMIT_SHA)
    manifest_path = tmp_path / "evidence-manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    result = verify_evidence_manifest(
        target_env="staging",
        manifest_path=manifest_path,
        expected_sha="different_sha_1234567890",
    )
    assert result is False


def test_anti_false_green_not_run_fails_closed(tmp_path: Path):
    manifest = create_manifest(
        classification="live",
        overall_status="PASS",
        passed=1,
        not_run=1,
    )
    manifest_path = tmp_path / "evidence-manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    result = verify_evidence_manifest(
        target_env="staging",
        manifest_path=manifest_path,
        expected_sha=SAMPLE_COMMIT_SHA,
    )
    assert result is False


def test_anti_false_green_zero_passed_fails_closed(tmp_path: Path):
    manifest = create_manifest(
        classification="live",
        overall_status="PASS",
        passed=0,
    )
    manifest_path = tmp_path / "evidence-manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    result = verify_evidence_manifest(
        target_env="staging",
        manifest_path=manifest_path,
        expected_sha=SAMPLE_COMMIT_SHA,
    )
    assert result is False


def test_missing_manifest_file_fails_closed(tmp_path: Path):
    non_existent = tmp_path / "missing-manifest.json"
    result = verify_evidence_manifest(
        target_env="staging",
        manifest_path=non_existent,
        expected_sha=SAMPLE_COMMIT_SHA,
    )
    assert result is False


# ======================================================================
# GAP-01: scripts/promote.py Preflight & Argument Mapping Regressions
# ======================================================================
import sys
import subprocess
from scripts.promote import (
    get_manifest_verify_cmd,
    resolve_source_sha,
    verify_promotion_preflight,
)


def test_get_manifest_verify_cmd_staging_maps_to_dev():
    cmd = get_manifest_verify_cmd("staging", SAMPLE_COMMIT_SHA)
    assert "--verify-manifest" in cmd
    assert "--env" in cmd
    assert cmd[cmd.index("--env") + 1] == "dev"
    assert "--expected-sha" in cmd
    assert cmd[cmd.index("--expected-sha") + 1] == SAMPLE_COMMIT_SHA


def test_get_manifest_verify_cmd_main_maps_to_staging():
    staging_sha = "d493122dd3c7f979affd3542218cd4bd815b362c"
    cmd = get_manifest_verify_cmd("main", staging_sha)
    assert "--verify-manifest" in cmd
    assert "--env" in cmd
    assert cmd[cmd.index("--env") + 1] == "staging"
    assert "--expected-sha" in cmd
    assert cmd[cmd.index("--expected-sha") + 1] == staging_sha


def test_get_manifest_verify_cmd_with_manifest_path(tmp_path: Path):
    manifest_file = tmp_path / "custom-manifest.json"
    cmd = get_manifest_verify_cmd("staging", SAMPLE_COMMIT_SHA, manifest_file)
    assert "--manifest" in cmd
    assert cmd[cmd.index("--manifest") + 1] == str(manifest_file)


def test_resolve_source_sha_resolves_branches(monkeypatch):
    executed_cmds = []
    mock_dev_sha = "640f5d766f6749dd07c0550c9f7baf5fefaff1e8"
    mock_staging_sha = "48a426cd71f5e89dadfc4ee32e8f85847b5ca88a"

    def mock_subprocess_run(cmd, *args, **kwargs):
        executed_cmds.append(cmd)
        if cmd[0] == "git" and len(cmd) >= 3 and cmd[1] == "rev-parse":
            branch = cmd[2]
            if branch == "Dev":
                return subprocess.CompletedProcess(args=cmd, returncode=0, stdout=f"{mock_dev_sha}\n", stderr="")
            if branch == "staging":
                return subprocess.CompletedProcess(args=cmd, returncode=0, stdout=f"{mock_staging_sha}\n", stderr="")
        return subprocess.CompletedProcess(args=cmd, returncode=1, stdout="", stderr="fatal: ambiguous argument")

    monkeypatch.setattr(subprocess, "run", mock_subprocess_run)

    dev_sha = resolve_source_sha("Dev")
    assert dev_sha == mock_dev_sha
    assert len(dev_sha) == 40
    assert all(c in "0123456789abcdefABCDEF" for c in dev_sha)
    assert ["git", "rev-parse", "Dev"] in executed_cmds

    staging_sha = resolve_source_sha("staging")
    assert staging_sha == mock_staging_sha
    assert len(staging_sha) == 40
    assert all(c in "0123456789abcdefABCDEF" for c in staging_sha)
    assert ["git", "rev-parse", "staging"] in executed_cmds


def test_resolve_source_sha_failure_raises_runtime_error(monkeypatch):
    def mock_subprocess_run(cmd, *args, **kwargs):
        return subprocess.CompletedProcess(
            args=cmd,
            returncode=128,
            stdout="",
            stderr="fatal: ambiguous argument 'unknown_branch'",
        )

    monkeypatch.setattr(subprocess, "run", mock_subprocess_run)
    with pytest.raises(RuntimeError) as exc_info:
        resolve_source_sha("unknown_branch")
    assert "Failed to resolve commit SHA for promotion source 'unknown_branch'" in str(exc_info.value)
    assert "fatal: ambiguous argument 'unknown_branch'" in str(exc_info.value)


def test_verify_promotion_preflight_aborts_on_manifest_failure(monkeypatch):
    calls = []

    def mock_subprocess_run(cmd, *args, **kwargs):
        calls.append(cmd)
        if cmd[0] == "git" and "rev-parse" in cmd:
            return subprocess.CompletedProcess(args=cmd, returncode=0, stdout=SAMPLE_COMMIT_SHA)
        if "--verify-manifest" in cmd:
            # Simulate failed manifest check (e.g. mocked or missing live evidence)
            return subprocess.CompletedProcess(args=cmd, returncode=1)
        # Base checks pass
        return subprocess.CompletedProcess(args=cmd, returncode=0)

    monkeypatch.setattr(subprocess, "run", mock_subprocess_run)

    with pytest.raises(SystemExit) as exc_info:
        verify_promotion_preflight("staging", "Dev")
    assert exc_info.value.code == 1

    # Verify base check, git rev-parse, and manifest check were invoked
    assert any("--verify-manifest" in c for c in calls)
    manifest_call = next(c for c in calls if "--verify-manifest" in c)
    assert "--env" in manifest_call
    assert manifest_call[manifest_call.index("--env") + 1] == "dev"
    assert "--expected-sha" in manifest_call
    assert manifest_call[manifest_call.index("--expected-sha") + 1] == SAMPLE_COMMIT_SHA


def test_verify_promotion_preflight_main_aborts_on_staging_manifest_failure(monkeypatch):
    calls = []

    def mock_subprocess_run(cmd, *args, **kwargs):
        calls.append(cmd)
        if cmd[0] == "git" and "rev-parse" in cmd:
            return subprocess.CompletedProcess(args=cmd, returncode=0, stdout="d493122dd3c7f979affd3542218cd4bd815b362c")
        if "--verify-manifest" in cmd:
            return subprocess.CompletedProcess(args=cmd, returncode=1)
        return subprocess.CompletedProcess(args=cmd, returncode=0)

    monkeypatch.setattr(subprocess, "run", mock_subprocess_run)

    with pytest.raises(SystemExit) as exc_info:
        verify_promotion_preflight("main", "staging")
    assert exc_info.value.code == 1

    assert any("--verify-manifest" in c for c in calls)
    manifest_call = next(c for c in calls if "--verify-manifest" in c)
    assert "--env" in manifest_call
    assert manifest_call[manifest_call.index("--env") + 1] == "staging"
    assert "--expected-sha" in manifest_call
    assert manifest_call[manifest_call.index("--expected-sha") + 1] == "d493122dd3c7f979affd3542218cd4bd815b362c"


def test_verify_promotion_preflight_aborts_on_base_check_failure(monkeypatch):
    calls = []

    def mock_subprocess_run(cmd, *args, **kwargs):
        calls.append(cmd)
        # Base checks fail
        return subprocess.CompletedProcess(args=cmd, returncode=1)

    monkeypatch.setattr(subprocess, "run", mock_subprocess_run)

    with pytest.raises(SystemExit) as exc_info:
        verify_promotion_preflight("staging", "Dev")
    assert exc_info.value.code == 1
    # Aborts before manifest check is reached
    assert len(calls) == 1


def test_verify_promotion_preflight_passes_when_all_checks_succeed(monkeypatch):
    calls = []

    def mock_subprocess_run(cmd, *args, **kwargs):
        calls.append(cmd)
        if cmd[0] == "git" and "rev-parse" in cmd:
            return subprocess.CompletedProcess(args=cmd, returncode=0, stdout=SAMPLE_COMMIT_SHA)
        return subprocess.CompletedProcess(args=cmd, returncode=0)

    monkeypatch.setattr(subprocess, "run", mock_subprocess_run)

    # Should complete without error
    verify_promotion_preflight("staging", "Dev")
    assert any("--verify-manifest" in c for c in calls)
    manifest_call = next(c for c in calls if "--verify-manifest" in c)
    assert manifest_call[manifest_call.index("--env") + 1] == "dev"
    assert manifest_call[manifest_call.index("--expected-sha") + 1] == SAMPLE_COMMIT_SHA


def test_verify_promotion_preflight_staging_accepts_valid_mocked_dev_manifest(tmp_path: Path, monkeypatch):
    manifest = create_manifest(classification="mocked", environment="dev", commit_sha=SAMPLE_COMMIT_SHA)
    manifest_path = tmp_path / "dev-evidence-manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    real_run = subprocess.run

    def mock_run(cmd, *args, **kwargs):
        if "--verify-manifest" not in cmd:
            if cmd[0] == "git" and "rev-parse" in cmd:
                return subprocess.CompletedProcess(args=cmd, returncode=0, stdout=SAMPLE_COMMIT_SHA)
            # Base quality checks pass
            return subprocess.CompletedProcess(args=cmd, returncode=0)
        return real_run(cmd, *args, **kwargs)

    monkeypatch.setattr(subprocess, "run", mock_run)

    # Valid mocked dev manifest must pass Dev preflight when promoting to staging
    verify_promotion_preflight("staging", "Dev", manifest_path=manifest_path)


def test_verify_promotion_preflight_main_rejects_mocked_staging_manifest(tmp_path: Path, monkeypatch):
    manifest = create_manifest(classification="mocked", environment="staging", commit_sha=SAMPLE_COMMIT_SHA)
    manifest_path = tmp_path / "mocked-staging-manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    real_run = subprocess.run

    def mock_run(cmd, *args, **kwargs):
        if "--verify-manifest" not in cmd:
            if cmd[0] == "git" and "rev-parse" in cmd:
                return subprocess.CompletedProcess(args=cmd, returncode=0, stdout=SAMPLE_COMMIT_SHA)
            return subprocess.CompletedProcess(args=cmd, returncode=0)
        return real_run(cmd, *args, **kwargs)

    monkeypatch.setattr(subprocess, "run", mock_run)

    # Mocked staging evidence must fail Staging preflight when promoting to main
    with pytest.raises(SystemExit) as exc_info:
        verify_promotion_preflight("main", "staging", manifest_path=manifest_path)
    assert exc_info.value.code == 1


def test_verify_promotion_preflight_aborts_on_sha_mismatch(tmp_path: Path, monkeypatch):
    manifest = create_manifest(classification="mocked", environment="dev", commit_sha="mismatched_sha_12345678901234567890123456789012")
    manifest_path = tmp_path / "dev-evidence-manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    real_run = subprocess.run

    def mock_run(cmd, *args, **kwargs):
        if "--verify-manifest" not in cmd:
            if cmd[0] == "git" and "rev-parse" in cmd:
                return subprocess.CompletedProcess(args=cmd, returncode=0, stdout=SAMPLE_COMMIT_SHA)
            return subprocess.CompletedProcess(args=cmd, returncode=0)
        return real_run(cmd, *args, **kwargs)

    monkeypatch.setattr(subprocess, "run", mock_run)

    # SHA mismatch must abort preflight
    with pytest.raises(SystemExit) as exc_info:
        verify_promotion_preflight("staging", "Dev", manifest_path=manifest_path)
    assert exc_info.value.code == 1


# ======================================================================
# GAP-02: Verifier Output Labels and Final Gate Verdict Regressions
# ======================================================================


def test_verifier_output_labels_mocked_staging_rejected(tmp_path: Path, capsys):
    manifest = create_manifest(classification="mocked", overall_status="PASS", environment="staging")
    manifest_path = tmp_path / "evidence-manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    result = verify_evidence_manifest(
        target_env="staging",
        manifest_path=manifest_path,
        expected_sha=SAMPLE_COMMIT_SHA,
    )
    assert result is False

    captured = capsys.readouterr()
    assert "Payload Self-Reported Status : PASS" in captured.out
    assert "Manifest Overall Status" not in captured.out
    assert "Classification violation: STAGING release gate requires 'live' execution evidence" in captured.out
    assert "❌ Evaluated Release Gate Verdict for STAGING: REJECTED (FAILED CLOSED)." in captured.out
    assert "Evaluated Release Gate Verdict for STAGING: PASSED." not in captured.out


def test_verifier_output_labels_mocked_prod_rejected(tmp_path: Path, capsys):
    manifest = create_manifest(classification="mocked", overall_status="PASS", environment="staging")
    manifest_path = tmp_path / "evidence-manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    result = verify_evidence_manifest(
        target_env="prod",
        manifest_path=manifest_path,
        expected_sha=SAMPLE_COMMIT_SHA,
    )
    assert result is False

    captured = capsys.readouterr()
    assert "Payload Self-Reported Status : PASS" in captured.out
    assert "Manifest Overall Status" not in captured.out
    assert "Classification violation: PROD release gate requires 'live' execution evidence" in captured.out
    assert "❌ Evaluated Release Gate Verdict for PROD: REJECTED (FAILED CLOSED)." in captured.out
    assert "Evaluated Release Gate Verdict for PROD: PASSED." not in captured.out


def test_verifier_output_labels_live_staging_accepted(tmp_path: Path, capsys):
    manifest = create_manifest(classification="live", overall_status="PASS", environment="staging")
    manifest_path = tmp_path / "evidence-manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    result = verify_evidence_manifest(
        target_env="staging",
        manifest_path=manifest_path,
        expected_sha=SAMPLE_COMMIT_SHA,
    )
    assert result is True

    captured = capsys.readouterr()
    assert "Payload Self-Reported Status : PASS" in captured.out
    assert "Manifest Overall Status" not in captured.out
    assert "✅ Evaluated Release Gate Verdict for STAGING: PASSED." in captured.out
    assert "REJECTED" not in captured.out


def test_verifier_output_labels_live_prod_accepted(tmp_path: Path, capsys):
    manifest = create_manifest(classification="live", overall_status="PASS", environment="staging")
    manifest_path = tmp_path / "evidence-manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    result = verify_evidence_manifest(
        target_env="prod",
        manifest_path=manifest_path,
        expected_sha=SAMPLE_COMMIT_SHA,
    )
    assert result is True

    captured = capsys.readouterr()
    assert "Payload Self-Reported Status : PASS" in captured.out
    assert "Manifest Overall Status" not in captured.out
    assert "✅ Evaluated Release Gate Verdict for PROD: PASSED." in captured.out
    assert "REJECTED" not in captured.out


def test_verifier_output_sha_mismatch_rejected(tmp_path: Path, capsys):
    manifest = create_manifest(classification="live", overall_status="PASS", commit_sha=SAMPLE_COMMIT_SHA)
    manifest_path = tmp_path / "evidence-manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    result = verify_evidence_manifest(
        target_env="staging",
        manifest_path=manifest_path,
        expected_sha="mismatched_commit_sha_12345",
    )
    assert result is False

    captured = capsys.readouterr()
    assert "Payload Self-Reported Status : PASS" in captured.out
    assert "Commit SHA mismatch" in captured.out
    assert "❌ Evaluated Release Gate Verdict for STAGING: REJECTED (FAILED CLOSED)." in captured.out
    assert "Evaluated Release Gate Verdict for STAGING: PASSED." not in captured.out


def test_verifier_output_missing_manifest_rejected(tmp_path: Path, capsys):
    missing_path = tmp_path / "missing-manifest.json"

    result = verify_evidence_manifest(
        target_env="staging",
        manifest_path=missing_path,
        expected_sha=SAMPLE_COMMIT_SHA,
    )
    assert result is False

    captured = capsys.readouterr()
    assert "Missing evidence manifest artifact" in captured.out
    assert "❌ Evaluated Release Gate Verdict for STAGING: REJECTED (FAILED CLOSED)." in captured.out


# ==============================================================================
# Ticket-Scoped Promotion Branch Support Tests (UPA-1401)
# ==============================================================================
from scripts.promote import (
    validate_ticket_format,
    derive_staging_promotion_branch,
    check_branch_exists,
)


def test_derive_staging_promotion_branch_valid_tickets():
    assert derive_staging_promotion_branch("upa-1401") == "promotion/upa-1401-staging"
    assert derive_staging_promotion_branch("UPA-1401") == "promotion/upa-1401-staging"
    assert derive_staging_promotion_branch("  upa-1305  ") == "promotion/upa-1305-staging"
    assert derive_staging_promotion_branch("SPRINT-12") == "promotion/sprint-12-staging"
    assert derive_staging_promotion_branch("jira-9999") == "promotion/jira-9999-staging"


@pytest.mark.parametrize(
    "invalid_ticket",
    [
        "",
        "   ",
        None,
        "1401",
        "-1401",
        "upa",
        "upa-",
        "upa_1401",
        "upa-abc",
        "promotion/upa-1401-staging",
        "upa-1401;rm -rf /",
        "upa-1401 && ls",
        "upa.1401",
    ],
)
def test_validate_ticket_format_rejects_malformed_inputs(invalid_ticket):
    with pytest.raises(ValueError):
        validate_ticket_format(invalid_ticket)


def test_check_branch_exists_locally(monkeypatch):
    def mock_subprocess_run(cmd, *args, **kwargs):
        if cmd[0] == "git" and "show-ref" in cmd:
            return subprocess.CompletedProcess(args=cmd, returncode=0, stdout="", stderr="")
        return subprocess.CompletedProcess(args=cmd, returncode=1, stdout="", stderr="")

    monkeypatch.setattr(subprocess, "run", mock_subprocess_run)
    exists, location = check_branch_exists("promotion/upa-1401-staging")
    assert exists is True
    assert location == "locally"


def test_check_branch_exists_remotely(monkeypatch):
    def mock_subprocess_run(cmd, *args, **kwargs):
        if cmd[0] == "git" and "show-ref" in cmd:
            return subprocess.CompletedProcess(args=cmd, returncode=1, stdout="", stderr="")
        if cmd[0] == "git" and "ls-remote" in cmd:
            return subprocess.CompletedProcess(
                args=cmd,
                returncode=0,
                stdout="b16fd8db5804cddaedab0cb2cbf81e85e0bbb338\trefs/heads/promotion/upa-1401-staging\n",
                stderr="",
            )
        return subprocess.CompletedProcess(args=cmd, returncode=1, stdout="", stderr="")

    monkeypatch.setattr(subprocess, "run", mock_subprocess_run)
    exists, location = check_branch_exists("promotion/upa-1401-staging")
    assert exists is True
    assert location == "remotely on origin"


def test_check_branch_exists_neither(monkeypatch):
    def mock_subprocess_run(cmd, *args, **kwargs):
        if cmd[0] == "git" and "show-ref" in cmd:
            return subprocess.CompletedProcess(args=cmd, returncode=1, stdout="", stderr="")
        if cmd[0] == "git" and "ls-remote" in cmd:
            return subprocess.CompletedProcess(args=cmd, returncode=0, stdout="", stderr="")
        return subprocess.CompletedProcess(args=cmd, returncode=1, stdout="", stderr="")

    monkeypatch.setattr(subprocess, "run", mock_subprocess_run)
    exists, location = check_branch_exists("promotion/upa-1401-staging")
    assert exists is False
    assert location == ""


def test_check_branch_exists_remote_error_raises_runtime_error(monkeypatch):
    def mock_subprocess_run(cmd, *args, **kwargs):
        if cmd[0] == "git" and "show-ref" in cmd:
            return subprocess.CompletedProcess(args=cmd, returncode=1, stdout="", stderr="")
        if cmd[0] == "git" and "ls-remote" in cmd:
            return subprocess.CompletedProcess(
                args=cmd,
                returncode=128,
                stdout="",
                stderr="fatal: Could not read from remote repository.",
            )
        return subprocess.CompletedProcess(args=cmd, returncode=1, stdout="", stderr="")

    monkeypatch.setattr(subprocess, "run", mock_subprocess_run)
    with pytest.raises(RuntimeError) as exc_info:
        check_branch_exists("promotion/upa-1401-staging")
    assert "Failed to query remote branch status on origin" in str(exc_info.value)
    assert "fatal: Could not read from remote repository." in str(exc_info.value)


def test_promote_cli_missing_ticket_for_staging_fails_closed(monkeypatch, capsys):
    import scripts.promote as promote_mod

    monkeypatch.setattr(sys, "argv", ["promote.py", "--to", "staging"])
    with pytest.raises(SystemExit) as exc_info:
        promote_mod.main()
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "--ticket is required when promoting to staging" in captured.out


def test_promote_cli_invalid_ticket_fails_closed(monkeypatch, capsys):
    import scripts.promote as promote_mod

    monkeypatch.setattr(sys, "argv", ["promote.py", "--to", "staging", "--ticket", "invalid_ticket"])
    with pytest.raises(SystemExit) as exc_info:
        promote_mod.main()
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Invalid ticket format 'invalid_ticket'" in captured.out


def test_promote_cli_existing_branch_fails_closed(monkeypatch, capsys):
    import scripts.promote as promote_mod

    monkeypatch.setattr(promote_mod, "check_branch_exists", lambda branch: (True, "locally"))
    monkeypatch.setattr(sys, "argv", ["promote.py", "--to", "staging", "--ticket", "upa-1401"])
    with pytest.raises(SystemExit) as exc_info:
        promote_mod.main()
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "already exists locally" in captured.out
    assert "Halting promotion safely to prevent destructive overwrite or reset." in captured.out


def test_promote_cli_remote_lookup_failure_fails_closed(monkeypatch, capsys):
    import scripts.promote as promote_mod

    def mock_check_branch_exists(branch):
        raise RuntimeError("fatal: Could not read from remote repository.")

    preflight_called = []
    def mock_preflight(*args, **kwargs):
        preflight_called.append(True)

    monkeypatch.setattr(promote_mod, "check_branch_exists", mock_check_branch_exists)
    monkeypatch.setattr(promote_mod, "verify_promotion_preflight", mock_preflight)
    monkeypatch.setattr(sys, "argv", ["promote.py", "--to", "staging", "--ticket", "upa-1401"])

    with pytest.raises(SystemExit) as exc_info:
        promote_mod.main()

    assert exc_info.value.code == 1
    assert len(preflight_called) == 0, "Preflight must not run if remote branch lookup fails"
    captured = capsys.readouterr()
    assert "🚨 RULE 2 FAIL-CLOSED: Remote branch verification failed" in captured.out
    assert "fatal: Could not read from remote repository." in captured.out
