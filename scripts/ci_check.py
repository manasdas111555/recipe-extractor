#!/usr/bin/env python3
"""
Pre-Merge CI & Quality Gate Validation Script
==============================================
Enforces the mandatory 3-stage contract before merging to Staging/Main:
1. Frontend Vitest suite (npm test)
2. Frontend Next.js production build (npm run build)
3. Backend pytest suite (pytest tests/)
"""

import sys
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

def run_step(cmd: str, cwd: Path, name: str) -> bool:
    print(f"\n==========================================")
    print(f"🚀 Running CI Step: {name}")
    print(f"Directory: {cwd}")
    print(f"Command:   {cmd}")
    print(f"==========================================\n")
    try:
        res = subprocess.run(cmd, cwd=cwd, shell=True, check=True)
        print(f"✅ {name} PASSED.")
        return True
    except subprocess.CalledProcessError as err:
        print(f"❌ {name} FAILED with exit code {err.returncode}.")
        return False

def main():
    frontend_dir = ROOT_DIR / "frontend"

    # Step 1: Frontend Vitest
    if not run_step("npm test", frontend_dir, "Frontend Vitest Suite"):
        sys.exit(1)

    # Step 2: Frontend Production Build
    if not run_step("npm run build", frontend_dir, "Frontend Production Build"):
        sys.exit(1)

    # Step 3: Backend Pytest Suite
    if not run_step("pytest tests/", ROOT_DIR, "Backend Pytest Suite"):
        sys.exit(1)

    print("\n🎉 ALL CI QUALITY GATES PASSED CLEANLY! Ready for staging promotion.\n")
    sys.exit(0)

if __name__ == "__main__":
    main()
