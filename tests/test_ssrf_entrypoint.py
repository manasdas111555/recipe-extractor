"""
SSRF Entry Point Validation Test (UPA-1201)
===========================================
Validates that public entry point validate_url_and_follow_redirects in url_validator.py
rejects URLs whose hostname resolves to private, loopback, or cloud metadata IP addresses.
"""

import pytest
import socket
from unittest.mock import patch
from backend.app.services.url_validator import validate_url_and_follow_redirects


def test_validate_url_and_follow_redirects_rejects_private_ip_resolution():
    """Asserts that validate_url_and_follow_redirects fails closed when DNS yields a private IP."""
    
    # 1. Test host resolving to loopback 127.0.0.1
    fake_addrinfoinfo_loopback = [
        (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("127.0.0.1", 443))
    ]
    with patch("socket.getaddrinfo", return_value=fake_addrinfoinfo_loopback):
        is_valid, err_msg, final_url = validate_url_and_follow_redirects("https://instagram.com/reel/test/")
        assert is_valid is False
        assert "private" in err_msg.lower() or "non-global" in err_msg.lower()

    # 2. Test host resolving to AWS metadata 169.254.169.254
    fake_addrinfoinfo_metadata = [
        (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("169.254.169.254", 443))
    ]
    with patch("socket.getaddrinfo", return_value=fake_addrinfoinfo_metadata):
        is_valid, err_msg, final_url = validate_url_and_follow_redirects("https://instagram.com/reel/test/")
        assert is_valid is False
        assert "private" in err_msg.lower() or "non-global" in err_msg.lower()

    # 3. Test host resolving to private LAN 192.168.1.100
    fake_addrinfoinfo_lan = [
        (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("192.168.1.100", 443))
    ]
    with patch("socket.getaddrinfo", return_value=fake_addrinfoinfo_lan):
        is_valid, err_msg, final_url = validate_url_and_follow_redirects("https://instagram.com/reel/test/")
        assert is_valid is False
        assert "private" in err_msg.lower() or "non-global" in err_msg.lower()
