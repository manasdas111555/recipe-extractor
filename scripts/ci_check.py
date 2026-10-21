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

# Force UTF-8 encoding on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

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

    # Step 1: TypeScript type checking (tsc --noEmit)
    if not run_step("npx tsc --noEmit", frontend_dir, "Frontend TypeScript Typecheck"):
        sys.exit(1)

    # Step 2: ESLint (npm run lint)
    if not run_step("npm run lint", frontend_dir, "Frontend ESLint Suite"):
        sys.exit(1)

    # Step 3: Frontend Vitest (npm test)
    if not run_step("npm test", frontend_dir, "Frontend Vitest Suite"):
        sys.exit(1)

    # Step 4: Frontend Production Build (npm run build)
    if not run_step("npm run build", frontend_dir, "Frontend Production Build"):
        sys.exit(1)

    # Step 5: Database Migration Parity & Grant Security Suite (UPA-1406)
    if not run_step("pytest tests/test_database_grants.py", ROOT_DIR, "Database Migration Parity & Grant Security Suite"):
        sys.exit(1)

    # Step 6: Backend Pytest Suite (pytest tests/)
    if not run_step("pytest tests/", ROOT_DIR, "Backend Pytest Suite"):
        sys.exit(1)

    # Optional: Mocked Playwright UI suite if --with-e2e flag provided
    if "--with-e2e" in sys.argv or "--with-mocked-e2e" in sys.argv:
        if not run_step("npm run test:e2e:mocked", frontend_dir, "Mocked Playwright E2E Suite"):
            sys.exit(1)

    print("\n🎉 ALL RULE 16 CI QUALITY GATES PASSED CLEANLY! Ready for staging promotion.\n")
    sys.exit(0)

if __name__ == "__main__":
    main()
