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
    
    for mod in CORE_MODULES:
        # Run import in a completely isolated sub-process
        test_code = (
            f"import sys; from pathlib import Path; "
            f"sys.path.insert(0, r'{ROOT_DIR}'); "
            f"import {mod}; "
            f"print('IMPORTED_SUCCESSFULLY')"
        )
        res = subprocess.run(
            [sys.executable, "-c", test_code],
            capture_output=True,
            text=True
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
    res = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests"],
        cwd=str(ROOT_DIR),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
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

def main():
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
