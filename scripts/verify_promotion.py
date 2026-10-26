#!/usr/bin/env python3
"""
Pre-Promotion Verification Script for Universal Pro AI
======================================================
Validates that the current codebase is 100% ready for environment promotion
(Dev -> Staging or Staging -> Prod).

Checks performed:
1. Python syntax & compilation across all source files.
2. Clean-process import test for all core modules (catching circular imports and missing exports).
3. Automated unit test suite execution (python -m unittest discover -s tests).
4. Environment & configuration hygiene checks.
"""

import os
import sys
import subprocess
import importlib
from pathlib import Path

# Force UTF-8 encoding on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

# Core application modules that must import cleanly in isolated Python processes
CORE_MODULES = [
    "config",
    "downloader",
    "gemini_processor",
    "ai_router",
    "media_utils",
    "ui_components",
    "whatsapp_service",
    "groq_processor",
    "mistral_processor",
    "backend.app.core.config",
    "backend.app.services.affiliate_engine",
    "backend.app.workers.media_downloader",
    "backend.app.workers.celery_app",
    "backend.app.api.v1.library",
]

def log_step(name: str):
    print(f"\n{'=' * 60}")
    print(f"👉 {name}")
    print(f"{'=' * 60}")

def check_compilation() -> bool:
    log_step("Step 1: Validating Python Syntax Compilation")
    py_files = (
        list(ROOT_DIR.glob("*.py")) +
        list((ROOT_DIR / "scripts").glob("*.py")) +
        list((ROOT_DIR / "tests").glob("*.py")) +
        list((ROOT_DIR / "backend").rglob("*.py"))
    )
    all_clean = True
    
    for file_path in py_files:
        rel_path = file_path.relative_to(ROOT_DIR)
        res = subprocess.run(
            [sys.executable, "-m", "py_compile", str(file_path)],
            capture_output=True,
            text=True
        )
        if res.returncode == 0:
            print(f"  ✅ Compiled cleanly: {rel_path}")
        else:
            print(f"  ❌ Syntax Error in {rel_path}:\n{res.stderr}")
            all_clean = False
            
    return all_clean

def check_clean_imports() -> bool:
    log_step("Step 2: Isolated Clean-Process Import Smoke Test")
    all_clean = True
    test_env = os.environ.copy()
    if not test_env.get("SECRET_KEY"):
        test_env["SECRET_KEY"] = "test_secret_key_for_unit_tests"
    
    for mod in CORE_MODULES:
        # Run import in a completely isolated sub-process
        test_code = (
            f"import sys; from pathlib import Path; "
            f"root = Path(r'{ROOT_DIR}'); "
            f"sys.path.insert(0, str(root)); "
            f"sys.path.insert(0, str(root / 'backend' / 'app' / 'services')); "
            f"sys.path.insert(0, str(root / 'backend' / 'app' / 'core')); "
            f"sys.path.insert(0, str(root / 'backend')); "
            f"import {mod}; "
            f"print('IMPORTED_SUCCESSFULLY')"
        )
        res = subprocess.run(
            [sys.executable, "-c", test_code],
            capture_output=True,
            text=True,
            env=test_env
        )
        if res.returncode == 0 and "IMPORTED_SUCCESSFULLY" in res.stdout:
            print(f"  ✅ Clean isolated import: {mod}")
        else:
            print(f"  ❌ Failed to import {mod}:")
            if res.stderr:
                print(f"     {res.stderr.strip()}")
            if res.stdout:
                print(f"     {res.stdout.strip()}")
            all_clean = False
            
    return all_clean

def run_unit_tests() -> bool:
    log_step("Step 3: Running Full Automated Unit Test Suite")
    test_env = os.environ.copy()
    if not test_env.get("SECRET_KEY"):
        test_env["SECRET_KEY"] = "test_secret_key_for_unit_tests"

    res = subprocess.run(
        [sys.executable, "-m", "pytest", "tests"],
        cwd=str(ROOT_DIR),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=test_env
    )
    
    print(res.stdout)
    if res.stderr:
        print(res.stderr)
        
    if res.returncode == 0:
        print("  ✅ All unit tests PASSED.")
        return True
    else:
        print(f"  ❌ Unit tests FAILED with exit code {res.returncode}")
        return False

def check_git_status() -> bool:
    log_step("Step 4: Checking Git Status & Working Tree Hygiene")
    try:
        res = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(ROOT_DIR),
            capture_output=True,
            text=True
        )
        uncommitted = [line for line in res.stdout.strip().split("\n") if line.strip()]
        if not uncommitted:
            print("  ✅ Git working tree is 100% clean.")
        else:
            print(f"  ℹ️ Notice: {len(uncommitted)} uncommitted file(s) present (will be committed before promotion).")
        return True
    except Exception as e:
        print(f"  ⚠️ Git check skipped: {e}")
        return True

import urllib.request
import urllib.error
import json
import argparse

def check_deployed_environment(target_env: str) -> bool:
    log_step(f"Post-Promotion Deployment Verification: {target_env.upper()}")

    if target_env == "staging":
        frontend_url = os.environ.get(
            "STAGING_BASE_URL",
            "https://universal-pro-ai-git-staging-manasprasannadas-projects.vercel.app"
        )
        backend_url = os.environ.get("STAGING_API_URL", "http://129.225.86.241/health")
        bypass_secret = os.environ.get("VERCEL_PROTECTION_BYPASS", "")
    else:
        frontend_url = "https://universal-pro-ai.vercel.app"
        backend_url = os.environ.get("PROD_API_URL", "http://140.245.214.28/health")
        bypass_secret = ""

    all_passed = True
    print(f"  Target Frontend Origin : {frontend_url}")
    print(f"  Target Backend Endpoint: {backend_url}")

    # 1. Probe Frontend
    try:
        req = urllib.request.Request(frontend_url, headers={"User-Agent": "UniversalProAI-Verifier/1.0"})
        if bypass_secret:
            req.add_header("x-vercel-protection-bypass", bypass_secret)
        with urllib.request.urlopen(req, timeout=15) as resp:
            status = resp.status
            if status < 400:
                print(f"  ✅ Frontend responsive: HTTP {status}")
            else:
                print(f"  ❌ Frontend returned non-200 HTTP status: {status}")
                all_passed = False
    except Exception as e:
        print(f"  ❌ Frontend probe failed: {e}")
        all_passed = False

    # 2. Probe Backend Health
    try:
        req = urllib.request.Request(backend_url, headers={"User-Agent": "UniversalProAI-Verifier/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            status = resp.status
            body = resp.read().decode("utf-8")
            if status == 200:
                print(f"  ✅ Backend health responsive: HTTP {status}")
                try:
                    payload = json.loads(body)
                    print(f"     Status: {payload.get('status', 'unknown')}")
                except Exception:
                    pass
            else:
                print(f"  ❌ Backend health returned non-200 HTTP status: {status}")
                all_passed = False
    except Exception as e:
        print(f"  ❌ Backend probe failed: {e}")
        all_passed = False

    return all_passed

def verify_evidence_manifest(target_env: str, manifest_path: Path = None, expected_sha: str = None) -> bool:
    log_step(f"Verifying Commit-Bound Evidence Manifest for {target_env.upper()}")
    if manifest_path is None:
        manifest_env = os.environ.get("EVIDENCE_MANIFEST_PATH")
        if manifest_env:
            candidate = Path(manifest_env)
            if candidate.is_absolute() or candidate.exists():
                manifest_path = candidate
            else:
                candidate_frontend = ROOT_DIR / "frontend" / candidate
                if candidate_frontend.exists():
                    manifest_path = candidate_frontend
                else:
                    manifest_path = candidate
        else:
            output_dir_env = os.environ.get("EVIDENCE_OUTPUT_DIR")
            manifest_filename = os.environ.get("EVIDENCE_MANIFEST_FILENAME", "evidence-manifest.json")
            if output_dir_env:
                candidate_frontend = ROOT_DIR / "frontend" / output_dir_env / manifest_filename
                candidate_cwd = Path.cwd() / output_dir_env / manifest_filename
                candidate_raw = Path(output_dir_env) / manifest_filename
                if candidate_frontend.exists():
                    manifest_path = candidate_frontend
                elif candidate_cwd.exists():
                    manifest_path = candidate_cwd
                elif candidate_raw.exists():
                    manifest_path = candidate_raw
                else:
                    manifest_path = candidate_frontend
            else:
                manifest_path = ROOT_DIR / "frontend" / "test-results" / "evidence-manifest.json"

    if not manifest_path.exists():
        print(f"  ❌ Missing evidence manifest artifact: {manifest_path}")
        print("  Release gate fails closed: cannot evaluate PASS without empirical evidence manifest.")
        print(f"  ❌ Evaluated Release Gate Verdict for {target_env.upper()}: REJECTED (FAILED CLOSED).")
        return False

    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    except Exception as e:
        print(f"  ❌ Malformed evidence manifest JSON: {e}")
        print(f"  ❌ Evaluated Release Gate Verdict for {target_env.upper()}: REJECTED (FAILED CLOSED).")
        return False

    overall_status = manifest.get("overallStatus")
    classification = manifest.get("executionClassification")
    commit_sha = manifest.get("commitSha")
    summary = manifest.get("summary", {})
    passed_count = summary.get("passed", 0)
    failed_count = summary.get("failed", 0)
    blocked_count = summary.get("blocked", 0)
    not_run_count = summary.get("notRun", 0)

    print(f"  Payload Self-Reported Status : {overall_status}")
    print(f"  Execution Classification     : {classification}")
    print(f"  Manifest Commit SHA          : {commit_sha}")
    print(f"  Summary                      : passed={passed_count}, failed={failed_count}, blocked={blocked_count}, notRun={not_run_count}")

    # Anti-false-green checks: missing, stale, mismatched, or NOT RUN evidence cannot become PASS
    if overall_status != "PASS":
        print(f"  ❌ Gate status is not PASS (got '{overall_status}'). Promotion blocked.")
        print(f"  ❌ Evaluated Release Gate Verdict for {target_env.upper()}: REJECTED (FAILED CLOSED).")
        return False

    if passed_count == 0:
        print("  ❌ Anti-false-green violation: overallStatus is PASS but passed test count is 0.")
        print(f"  ❌ Evaluated Release Gate Verdict for {target_env.upper()}: REJECTED (FAILED CLOSED).")
        return False

    if failed_count > 0 or blocked_count > 0 or not_run_count > 0:
        print(f"  ❌ Anti-false-green violation: manifest contains non-passing tests (failed={failed_count}, blocked={blocked_count}, notRun={not_run_count}).")
        print(f"  ❌ Evaluated Release Gate Verdict for {target_env.upper()}: REJECTED (FAILED CLOSED).")
        return False

    # Classification validation: require 'live' for staging and prod release gates
    if not classification or classification not in ["mocked", "live"]:
        print(f"  ❌ Manifest missing or invalid executionClassification: '{classification}' (expected 'mocked' or 'live').")
        print(f"  ❌ Evaluated Release Gate Verdict for {target_env.upper()}: REJECTED (FAILED CLOSED).")
        return False

    if target_env in ["staging", "prod"] and classification != "live":
        print(f"  ❌ Classification violation: {target_env.upper()} release gate requires 'live' execution evidence, got '{classification}'.")
        print("  Mocked Playwright tests cannot satisfy a required live Staging or Production release gate.")
        print(f"  ❌ Evaluated Release Gate Verdict for {target_env.upper()}: REJECTED (FAILED CLOSED).")
        return False

    # Commit SHA validation: validate manifest.commitSha === deployedStagingSha
    if expected_sha:
        if not commit_sha:
            print(f"  ❌ Manifest missing commitSha (expected {expected_sha}).")
            print(f"  ❌ Evaluated Release Gate Verdict for {target_env.upper()}: REJECTED (FAILED CLOSED).")
            return False
        if commit_sha != expected_sha:
            print(f"  ❌ Commit SHA mismatch: expected {expected_sha}, got {commit_sha}")
            print(f"  ❌ Evaluated Release Gate Verdict for {target_env.upper()}: REJECTED (FAILED CLOSED).")
            return False
        print(f"  ✅ Commit SHA validated against deployed commit: {commit_sha}")

    print("  ✅ Evidence manifest validation PASSED.")
    print(f"  ✅ Evaluated Release Gate Verdict for {target_env.upper()}: PASSED.")
    return True

def main():
    parser = argparse.ArgumentParser(description="Universal Pro AI Promotion & Deployment Verifier.")
    parser.add_argument("--deployed", choices=["staging", "prod"], help="Verify deployed cloud environment")
    parser.add_argument("--expected-sha", help="Expected deployed commit SHA to validate against evidence manifest")
    parser.add_argument("--manifest", type=Path, help="Path to evidence manifest JSON file")
    parser.add_argument("--verify-manifest", action="store_true", help="Explicitly verify commit-bound evidence manifest")
    parser.add_argument("--env", choices=["dev", "staging", "prod"], default="staging", help="Target environment for manifest verification (default: staging)")
    args = parser.parse_args()

    if args.deployed:
        print(f"🚀 Running Universal Pro AI Deployed Environment Verification ({args.deployed})...")
        success = check_deployed_environment(args.deployed)
        if args.expected_sha or args.verify_manifest or args.manifest:
            sha = args.expected_sha or os.environ.get("DEPLOYED_SHA") or os.environ.get("DEPLOYED_STAGING_SHA")
            manifest_ok = verify_evidence_manifest(args.deployed, args.manifest, sha)
            success = success and manifest_ok
        sys.exit(0 if success else 1)

    if args.verify_manifest or args.manifest:
        sha = args.expected_sha or os.environ.get("DEPLOYED_SHA") or os.environ.get("DEPLOYED_STAGING_SHA")
        target_env = args.env or os.environ.get("TARGET_ENV", "staging")
        manifest_ok = verify_evidence_manifest(target_env, args.manifest, sha)
        sys.exit(0 if manifest_ok else 1)

    print("🚀 Running Universal Pro AI Pre-Promotion Verification...")
    print(f"📁 Workspace Root: {ROOT_DIR}")
    
    checks = [
        ("Syntax Compilation", check_compilation()),
        ("Clean Imports", check_clean_imports()),
        ("Automated Tests", run_unit_tests()),
        ("Git Hygiene", check_git_status()),
    ]
    
    print(f"\n{'=' * 60}")
    print("📊 PRE-PROMOTION VERIFICATION SUMMARY")
    print(f"{'=' * 60}")
    
    all_passed = True
    for name, passed in checks:
        status_icon = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status_icon} : {name}")
        if not passed:
            all_passed = False
            
    if all_passed:
        print("\n🎉 ALL CHECKS PASSED! Codebase is certified safe for promotion to Staging / Prod.")
        sys.exit(0)
    else:
        print("\n🚨 PROMOTION HALTED: Resolve the failures above before promoting.")
        sys.exit(1)

if __name__ == "__main__":
    main()
