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

import re
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
    """Construct command to verify the release evidence manifest for the source branch being promoted."""
    # When promoting Dev -> staging, verify the Dev manifest (source)
    # When promoting staging -> main, verify the Staging live manifest (source)
    verify_env = "dev" if target_env == "staging" else "staging"
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
    verify_env = "dev" if target_env == "staging" else "staging"
    print(f"\n👉 Verifying release evidence manifest for [{target_env}] (source: {source_env} @ {expected_sha[:10]})...")

    manifest_cmd = get_manifest_verify_cmd(target_env, expected_sha, manifest_path)
    manifest_res = subprocess.run(manifest_cmd)
    if manifest_res.returncode != 0:
        print(
            f"\n🚨 ABORTING: Mandatory {verify_env.upper()} release evidence manifest verification failed "
            f"for source revision {expected_sha}. Promotion halted."
        )
        sys.exit(1)

def validate_ticket_format(ticket: str) -> str:
    """Validate and normalize a Jira / Backlog ticket identifier.

    Must follow the standard pattern: '<prefix>-<number>' (e.g., 'upa-1401' or 'UPA-1401').
    Returns the normalized lower-cased ticket string.
    """
    if not ticket or not isinstance(ticket, str):
        raise ValueError("Ticket identifier cannot be empty.")
    normalized = ticket.strip().lower()
    if not re.match(r"^[a-z]+-\d+$", normalized):
        raise ValueError(
            f"Invalid ticket format '{ticket}'. Must match pattern '<prefix>-<number>' (e.g. 'upa-1401' or 'UPA-1401')."
        )
    return normalized

def derive_staging_promotion_branch(ticket: str) -> str:
    """Derive the mandated ticket-scoped promotion branch name for staging promotion.

    Example: 'upa-1401' -> 'promotion/upa-1401-staging'
    """
    normalized_ticket = validate_ticket_format(ticket)
    return f"promotion/{normalized_ticket}-staging"

def check_branch_exists(branch_name: str) -> tuple:
    """Check whether a target branch already exists locally or on remote 'origin'.

    Returns (exists: bool, location: str).
    Raises RuntimeError if remote branch state cannot be verified (e.g. network/auth failure).
    """
    # 1. Local ref check
    local_res = subprocess.run(
        ["git", "show-ref", "--verify", "--quiet", f"refs/heads/{branch_name}"],
        cwd=str(ROOT_DIR),
        text=True,
        capture_output=True,
    )
    if local_res.returncode == 0:
        return True, "locally"

    # 2. Remote ref check on origin
    remote_res = subprocess.run(
        ["git", "ls-remote", "--heads", "origin", branch_name],
        cwd=str(ROOT_DIR),
        text=True,
        capture_output=True,
    )
    if remote_res.returncode != 0:
        error_msg = remote_res.stderr.strip() if remote_res.stderr else f"git exit code {remote_res.returncode}"
        raise RuntimeError(
            f"Failed to query remote branch status on origin: {error_msg}. "
            "Unable to verify whether branch already exists remotely."
        )

    if remote_res.stdout.strip():
        return True, "remotely on origin"

    return False, ""

def main():
    parser = argparse.ArgumentParser(description="Promote code safely across environments.")
    parser.add_argument("--to", choices=["staging", "main"], required=True, help="Target environment to promote into")
    parser.add_argument("--ticket", type=str, help="Ticket identifier for ticket-scoped promotion branch (e.g., 'upa-1401')")
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

    # Enforce Rule 2 ticket-scoped branch requirement for staging promotion
    promo_branch = None
    if target_env == "staging":
        if not args.ticket:
            print("\n🚨 RULE 2 FAIL-CLOSED: --ticket is required when promoting to staging (e.g. --ticket upa-1401).")
            sys.exit(1)
        try:
            promo_branch = derive_staging_promotion_branch(args.ticket)
        except ValueError as err:
            print(f"\n🚨 RULE 2 FAIL-CLOSED: {err}")
            sys.exit(1)

        # Early check: ensure target promotion branch does not already exist
        try:
            exists, location = check_branch_exists(promo_branch)
        except RuntimeError as err:
            print(f"\n🚨 RULE 2 FAIL-CLOSED: Remote branch verification failed: {err}")
            sys.exit(1)

        if exists:
            print(
                f"\n🚨 RULE 2 FAIL-CLOSED: Target promotion branch '{promo_branch}' already exists {location}. "
                "Halting promotion safely to prevent destructive overwrite or reset."
            )
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
        # Re-check existence post-pull to ensure remote sync didn't fetch it
        try:
            exists, location = check_branch_exists(promo_branch)
        except RuntimeError as err:
            print(f"\n🚨 RULE 2 FAIL-CLOSED: Remote branch verification failed: {err}")
            sys.exit(1)

        if exists:
            print(
                f"\n🚨 RULE 2 FAIL-CLOSED: Target promotion branch '{promo_branch}' already exists {location}. "
                "Halting promotion safely to prevent destructive overwrite or reset."
            )
            sys.exit(1)

        print(f"\n👉 Creating isolated promotion branch: {promo_branch}...")
        run_cmd(["git", "checkout", "-b", promo_branch])
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
