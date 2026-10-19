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

def resolve_source_sha(source_env: str) -> str:
    """Resolve the authoritative 40-character commit SHA of the source branch being promoted."""
    res = subprocess.run(
        ["git", "rev-parse", source_env],
        cwd=str(ROOT_DIR),
        text=True,
        capture_output=True,
    )
    if res.returncode != 0:
        raise RuntimeError(f"Failed to resolve commit SHA for promotion source '{source_env}': {res.stderr.strip() if res.stderr else 'unknown error'}")
    return (res.stdout or "").strip()

def get_manifest_verify_cmd(target_env: str, expected_sha: str, manifest_path: Path = None) -> list:
    """Construct command to verify the release evidence manifest for the given target environment."""
    verify_env = "staging" if target_env == "staging" else "prod"
    cmd = [
        sys.executable,
        str(ROOT_DIR / "scripts" / "verify_promotion.py"),
        "--verify-manifest",
        "--env",
        verify_env,
        "--expected-sha",
        expected_sha,
    ]
    if manifest_path:
        cmd.extend(["--manifest", str(manifest_path)])
    return cmd

def verify_promotion_preflight(target_env: str, source_env: str, manifest_path: Path = None) -> None:
    """Execute pre-promotion code quality checks and mandatory commit-bound evidence manifest validation."""
    # 1. Base Pre-Promotion Verification (compilation, imports, automated tests, git hygiene)
    print("\n👉 Running quality gate verification...")
    verify_res = subprocess.run([sys.executable, str(ROOT_DIR / "scripts" / "verify_promotion.py")])
    if verify_res.returncode != 0:
        print("\n🚨 ABORTING: Pre-promotion verification checks failed. Fix issues before promoting.")
        sys.exit(1)

    # 2. Mandatory Release Evidence Manifest Verification
    expected_sha = resolve_source_sha(source_env)
    verify_env = "staging" if target_env == "staging" else "prod"
    print(f"\n👉 Verifying release evidence manifest for [{target_env}] (source: {source_env} @ {expected_sha[:10]})...")

    manifest_cmd = get_manifest_verify_cmd(target_env, expected_sha, manifest_path)
    manifest_res = subprocess.run(manifest_cmd)
    if manifest_res.returncode != 0:
        print(
            f"\n🚨 ABORTING: Mandatory {verify_env.upper()} release evidence manifest verification failed "
            f"for source revision {expected_sha}. Promotion halted."
        )
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Promote code safely across environments.")
    parser.add_argument("--to", choices=["staging", "main"], required=True, help="Target environment to promote into")
    parser.add_argument("--owner-approved", action="store_true", help="Confirm explicit written owner authorization exists in docs/po-governance/SIGN_OFF.md")
    parser.add_argument("--manifest", type=Path, help="Optional path to evidence manifest JSON file")
    args = parser.parse_args()

    target_env = args.to
    source_env = "Dev" if target_env == "staging" else "staging"

    # Enforce Rule 2 strict production gate
    if target_env == "main":
        if not args.owner_approved:
            print("\n🚨 RULE 2 STRICT PRODUCTION GATE VIOLATION:")
            print("  Promotion to main requires explicit, written prior sign-off from the repository owner.")
            print("  Record approval in docs/po-governance/SIGN_OFF.md and re-run with --owner-approved.")
            sys.exit(1)

        sign_off_file = ROOT_DIR / "docs" / "po-governance" / "SIGN_OFF.md"
        if not sign_off_file.exists():
            print(f"\n🚨 RULE 2 FAIL-CLOSED: Missing required sign-off log: {sign_off_file}")
            sys.exit(1)

        sign_off_content = sign_off_file.read_text(encoding="utf-8", errors="replace")
        if "PO Approved" not in sign_off_content and "PO-Approved" not in sign_off_content:
            print("\n🚨 RULE 2 FAIL-CLOSED: No explicit owner sign-off entry found in docs/po-governance/SIGN_OFF.md.")
            sys.exit(1)

    print(f"\n🚀 Initiating Safe Promotion: [{source_env}] ──> [{target_env}]")
    print(f"{'=' * 60}")

    # 1. Run Pre-Promotion Verification & Evidence Manifest Verification
    verify_promotion_preflight(target_env, source_env, args.manifest)

    # 2. Verify current branch
    current_branch_res = run_cmd(["git", "branch", "--show-current"])
    current_branch = current_branch_res.stdout.strip()

    if current_branch != source_env:
        print(f"⚠️ Switching to source branch: {source_env}")
        run_cmd(["git", "checkout", source_env])

    # 3. Pull latest source
    print(f"\n👉 Syncing {source_env} with remote...")
    run_cmd(["git", "pull", "origin", source_env], check=False)

    # 4. Governed Promotion Workflow: Staging vs Production
    if target_env == "staging":
        # Rule 2 Phase 4: Prepare isolated promotion branch and submit PR
        sha_res = run_cmd(["git", "rev-parse", "--short", "HEAD"])
        head_sha = sha_res.stdout.strip()
        promo_branch = f"promotion/staging-{head_sha}"

        print(f"\n👉 Creating isolated promotion branch: {promo_branch}...")
        run_cmd(["git", "checkout", "-B", promo_branch])
        print(f"👉 Pushing promotion branch to origin: {promo_branch}...")
        run_cmd(["git", "push", "-u", "origin", promo_branch])

        # Return to Dev immediately
        print("👉 Returning to Dev branch...")
        run_cmd(["git", "checkout", "Dev"])

        print(f"\n✅ Phase 4 Governed Staging Promotion Branch Prepared:")
        print(f"  Branch '{promo_branch}' pushed to origin.")
        print("  Next Required Governed Steps (Rule 2 Phase 4):")
        print(f"  1. Submit PR from '{promo_branch}' into 'staging'.")
        print("  2. Validate remote GitHub Actions CI checks (ci.yml).")
        print("  3. Obtain explicit Product Owner / Repository Owner approval on the PR.")
        print("  4. Merge PR into origin/staging via GitHub PR merge.")
        print("  Direct merges or direct pushes to staging are strictly blocked by governance.\n")
        sys.exit(0)

    # Production Promotion (staging -> main)
    # 5. Checkout main and merge from staging
    print(f"\n👉 Checking out target branch: main...")
    run_cmd(["git", "checkout", "main"])
    run_cmd(["git", "pull", "origin", "main"], check=False)

    print(f"\n👉 Merging staging into main under explicit owner authorization...")
    run_cmd(["git", "merge", "staging", "--no-edit", "-m", f"chore(release): promote staging to main [OWNER APPROVED]"])

    print(f"\n👉 Pushing to origin/main...")
    run_cmd(["git", "push", "origin", "main"])

    print(f"\n👉 Returning to active development branch: Dev...")
    run_cmd(["git", "checkout", "Dev"])

    print(f"\n🎉 Production promotion to [main] COMPLETED SUCCESSFULLY! Returning to 'Dev'.\n")

if __name__ == "__main__":
    main()
