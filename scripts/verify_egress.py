#!/usr/bin/env python3
"""
Universal Pro AI — Container Egress Firewall Verification Tool
===============================================================
Executes inside the container to verify network egress security controls:
1. Environment Telemetry: OS, Hostname/Container ID, Python version.
2. Failure Type Categorization: REFUSED, UNREACHABLE, TIMEOUT, BLOCKED.
3. Strict Exit Gate: Returns exit code 0 ONLY if metadata and private targets FAIL and allowed host SUCCEEDS.
"""

import sys
import os
import platform
import socket
import urllib.request
import urllib.error

def get_container_id() -> str:
    """Extracts container ID from hostname or /proc/self/cgroup."""
    cid = os.environ.get("HOSTNAME", socket.gethostname())
    if os.path.exists("/proc/self/cgroup"):
        try:
            with open("/proc/self/cgroup", "r") as f:
                for line in f:
                    parts = line.strip().split("/")
                    if len(parts) > 2 and len(parts[-1]) == 64:
                        return parts[-1][:12]
        except Exception:
            pass
    return cid

def print_environment_info():
    print("=" * 70)
    print("UNIVERSAL PRO AI — CONTAINER EGRESS FIREWALL VERIFICATION")
    print("=" * 70)
    print(f"OS Platform     : {platform.system()} {platform.release()} ({platform.machine()})")
    print(f"Hostname/CID    : {socket.gethostname()} (Container ID: {get_container_id()})")
    print(f"Python Version  : {sys.version.split()[0]} ({sys.executable})")
    print("=" * 70)

def test_egress_target(target_url: str, is_allowed_target: bool) -> bool:
    print(f"[*] Testing target: {target_url:45s} -> ", end="", flush=True)
    try:
        req = urllib.request.Request(
            target_url,
            headers={"User-Agent": "UniversalProAI-EgressVerification/2.0"}
        )
        with urllib.request.urlopen(req, timeout=3) as response:
            status = response.status
            if is_allowed_target:
                print(f"[SUCCESS] Connected (HTTP {status})")
                return True
            else:
                print(f"[SECURITY VULNERABILITY] Unexpected connection established (HTTP {status})")
                return False
    except urllib.error.HTTPError as e:
        if is_allowed_target:
            print(f"[SUCCESS] Reached target host (HTTP {e.code})")
            return True
        else:
            print(f"[SECURITY VULNERABILITY] HTTP error returned from blocked host (HTTP {e.code})")
            return False
    except urllib.error.URLError as e:
        reason_str = str(e.reason)
        failure_type = "BLOCKED"
        if "Connection refused" in reason_str or "10061" in reason_str:
            failure_type = "REFUSED"
        elif "Network is unreachable" in reason_str or "10051" in reason_str or "No route to host" in reason_str:
            failure_type = "UNREACHABLE"
        elif "timed out" in reason_str:
            failure_type = "TIMEOUT"
            
        if not is_allowed_target:
            print(f"[BLOCKED AS EXPECTED] ({failure_type}: {e.reason})")
            return True
        else:
            print(f"[FAILED] Allowed target unreachable ({failure_type}: {e.reason})")
            return False
    except socket.timeout:
        if not is_allowed_target:
            print("[BLOCKED AS EXPECTED] (TIMEOUT)")
            return True
        else:
            print("[FAILED] Connection timed out for allowed target")
            return False
    except Exception as e:
        if not is_allowed_target:
            print(f"[BLOCKED AS EXPECTED] ({type(e).__name__}: {e})")
            return True
        else:
            print(f"[FAILED] Unexpected error ({type(e).__name__}: {e})")
            return False

def main():
    print_environment_info()

    results = []

    # 1. AWS/Cloud Metadata Endpoint (169.254.169.254) — MUST FAIL
    results.append(test_egress_target("http://169.254.169.254/latest/meta-data/", is_allowed_target=False))

    # 2. Private Subnet IP (10.0.0.1) — MUST FAIL
    results.append(test_egress_target("http://10.0.0.1/", is_allowed_target=False))

    # 3. Private Subnet IP (192.168.1.1) — MUST FAIL
    results.append(test_egress_target("http://192.168.1.1/", is_allowed_target=False))

    # 4. Public Social Host (www.instagram.com) — MUST SUCCEED
    results.append(test_egress_target("https://www.instagram.com/", is_allowed_target=True))

    print("-" * 70)
    all_passed = all(results)
    if all_passed:
        print("RESULT: ALL CONTAINER EGRESS FIREWALL CHECKS PASSED [OK]")
        sys.exit(0)
    else:
        print("RESULT: CONTAINER EGRESS FIREWALL CHECKS FAILED [FAIL]")
        sys.exit(1)

if __name__ == "__main__":
    main()
