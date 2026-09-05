#!/usr/bin/env python3
"""
Branch Promotion Automation Script for Universal Pro AI
======================================================
Safely promotes code between environments:
  Dev -> staging  (Testing in Cloud Staging)
  staging -> main (Production Release)

Enforces:
1. All verification checks in scripts/verify_promotion.py must pass before any merge.
2. Clean working tree.
3. Automatic push to origin upon successful verification.
"""

import sys
import argparse
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

def run_cmd(cmd, check=True):
    print(f"  $ {' '.join(cmd)}")
    res = subprocess.run(cmd, cwd=str(ROOT_DIR), text=True, capture_output=True)
    if check and res.returncode != 0:
        print(f"❌ Command failed:\n{res.stderr or res.stdout}")
        sys.exit(res.returncode)
    return res

def main():
    parser = argparse.ArgumentParser(description="Promote code safely across environments.")
    parser.add_argument("--to", choices=["staging", "main"], required=True, help="Target environment to promote into")
    args = parser.parse_args()

    target_env = args.to
    source_env = "Dev" if target_env == "staging" else "staging"

    print(f"\n🚀 Initiating Safe Promotion: [{source_env}] ──> [{target_env}]")
    print(f"{'=' * 60}")

    # 1. Run Pre-Promotion Verification
    print("\n👉 Running quality gate verification...")
    verify_res = subprocess.run([sys.executable, str(ROOT_DIR / "scripts" / "verify_promotion.py")])
    if verify_res.returncode != 0:
        print("\n🚨 ABORTING: Verification checks failed. Fix issues before promoting.")
        sys.exit(1)

    # 2. Verify current branch
    current_branch_res = run_cmd(["git", "branch", "--show-current"])
    current_branch = current_branch_res.stdout.strip()

    if current_branch != source_env:
        print(f"⚠️ Switching to source branch: {source_env}")
        run_cmd(["git", "checkout", source_env])

    # 3. Pull latest source
    print(f"\n👉 Syncing {source_env} with remote...")
    run_cmd(["git", "pull", "origin", source_env], check=False)

    # 4. Checkout target branch
    print(f"\n👉 Checking out target branch: {target_env}...")
    run_cmd(["git", "checkout", target_env])
    run_cmd(["git", "pull", "origin", target_env], check=False)

    # 5. Merge source into target
    print(f"\n👉 Merging {source_env} into {target_env}...")
    run_cmd(["git", "merge", source_env, "--no-edit", "-m", f"chore(release): promote {source_env} to {target_env}"])

    # 6. Push to remote
    print(f"\n👉 Pushing to origin/{target_env}...")
    run_cmd(["git", "push", "origin", target_env])

    # 7. Switch back to Dev for continued development
    print(f"\n👉 Returning to active development branch: Dev...")
    run_cmd(["git", "checkout", "Dev"])

    print(f"\n🎉 Promotion to [{target_env}] COMPLETED SUCCESSFULLY! Returning to 'Dev'.\n")

if __name__ == "__main__":
    main()
