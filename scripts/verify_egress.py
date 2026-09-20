#!/usr/bin/env python3
"""
Container Egress Firewall Verification Script
==============================================
Verifies that worker and API runtime containers correctly enforce egress network security:
1. Cloud metadata IP (169.254.169.254) requests -> FAIL
2. Private RFC1918 IP (10.0.0.1) requests -> FAIL
3. Public allowlisted social host (https://www.instagram.com) -> SUCCEED
"""

import sys
import urllib.request
import socket

def test_egress_endpoint(target_url: str, expected_success: bool) -> bool:
    print(f"Testing egress connection to: {target_url} ... ", end="")
    try:
        req = urllib.request.Request(
            target_url,
            headers={"User-Agent": "UniversalProAI-EgressCheck/1.0"}
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            status = resp.status
            if expected_success and status in [200, 301, 302, 403, 404]:
                print(f"SUCCESS (HTTP {status})")
                return True
            elif not expected_success:
                print(f"FAILED SECURITY TEST (Unexpectedly connected with HTTP {status})")
                return False
    except Exception as e:
        if not expected_success:
            print(f"BLOCKED AS EXPECTED ({type(e).__name__}: {e})")
            return True
        else:
            print(f"FAILED EXPECTED CONNECTION ({type(e).__name__}: {e})")
            return False
    return False

def main():
    print("=" * 60)
    print("Universal Pro AI — Container Egress Firewall Verification")
    print("=" * 60)

    results = []
    # Test 1: Cloud metadata IP (must FAIL)
    results.append(test_egress_endpoint("http://169.254.169.254/latest/meta-data/", expected_success=False))

    # Test 2: Private RFC1918 range IP (must FAIL)
    results.append(test_egress_endpoint("http://10.0.0.1/", expected_success=False))

    # Test 3: Public allowlisted social host (must SUCCEED)
    results.append(test_egress_endpoint("https://www.instagram.com/", expected_success=True))

    print("-" * 60)
    if all(results):
        print("RESULT: ALL EGRESS FIREWALL CHECKS PASSED [OK]")
        sys.exit(0)
    else:
        print("RESULT: EGRESS FIREWALL CHECKS FAILED [FAIL]")
        sys.exit(1)

if __name__ == "__main__":
    main()
