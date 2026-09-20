"""
Universal Security URL & Host Allowlist Validator (UPA-Security)
================================================================
Enforces strict URL validation, domain allowlisting, SSRF protection with IP pinning,
and open-redirect defenses.
"""

import socket
import ipaddress
import urllib.parse
import hmac
import hashlib
from typing import Tuple, Optional, List
import logging

logger = logging.getLogger(__name__)

ALLOWED_DOMAINS = {
    "instagram.com",
    "youtube.com",
    "youtu.be",
    "tiktok.com",
    "facebook.com",
    "fb.watch",
}

ALLOWED_MERCHANT_DOMAINS = {
    "amazon.in",
    "amazon.com",
    "flipkart.com",
    "meesho.com",
    "myntra.com",
    "blinkit.com",
    "zepto.now",
    "instamart.com",
    "bigbasket.com",
    "jiomart.com",
}


def is_allowed_domain(hostname: str, allowed_set=ALLOWED_DOMAINS) -> bool:
    """Checks whether hostname matches an allowed domain exactly or as a subdomain."""
    if not hostname:
        return False
    host = hostname.lower().strip()
    
    # Reject raw IP addresses (numeric or IPv6)
    try:
        ipaddress.ip_address(host)
        return False
    except ValueError:
        pass

    for domain in allowed_set:
        if host == domain or host.endswith("." + domain):
            return True
    return False


def unwrap_ip(ip_str: str) -> str:
    """Unwraps IPv4-mapped IPv6 addresses (e.g., ::ffff:192.168.1.1 -> 192.168.1.1)."""
    try:
        ip_obj = ipaddress.ip_address(ip_str)
        if isinstance(ip_obj, ipaddress.IPv6Address) and ip_obj.ipv4_mapped:
            return str(ip_obj.ipv4_mapped)
        return str(ip_obj)
    except ValueError:
        return ip_str


def is_globally_routable_ip(ip_str: str) -> bool:
    """Verifies that an IP is globally routable and not private/loopback/link-local/metadata."""
    try:
        clean_ip = unwrap_ip(ip_str)
        ip = ipaddress.ip_address(clean_ip)
        return ip.is_global
    except ValueError:
        return False


def resolve_and_validate_hostname(hostname: str) -> Tuple[bool, Optional[str], str]:
    """
    Resolves a hostname via socket.getaddrinfo, validates the target pinned IP,
    and returns (is_valid, pinned_ip, error_message).
    """
    try:
        addr_info = socket.getaddrinfo(hostname, 443, socket.AF_UNSPEC, socket.SOCK_STREAM)
        if not addr_info:
            return False, None, f"Could not resolve hostname {hostname}"

        first_ip = unwrap_ip(addr_info[0][4][0])
        if not is_globally_routable_ip(first_ip):
            return False, None, f"Host {hostname} resolved to non-global/private IP {first_ip}"

        return True, first_ip, ""
    except socket.gaierror as e:
        return False, None, f"DNS resolution failed for {hostname}: {e}"
    except Exception as e:
        return False, None, f"Host validation error: {e}"


def validate_social_url(url: str, max_redirects: int = 3) -> Tuple[bool, str, Optional[str], Optional[str]]:
    """
    Validates a social video URL against scheme, credentials, ports, allowlist, and SSRF rules.
    Returns (is_valid, error_message, clean_hostname, pinned_ip).
    """
    if not url or not isinstance(url, str):
        return False, "URL must be a non-empty string", None, None

    url_str = url.strip()

    # Parse URL
    try:
        parts = urllib.parse.urlsplit(url_str)
    except Exception as e:
        return False, f"Invalid URL structure: {e}", None, None

    # Scheme must be https
    if parts.scheme.lower() != "https":
        return False, "Only HTTPS URLs are allowed", None, None

    # Reject credentials in URL
    if parts.username or parts.password:
        return False, "URLs containing user credentials are prohibited", None, None

    # Hostname required
    hostname = parts.hostname
    if not hostname:
        return False, "URL missing valid hostname", None, None
    hostname = hostname.lower()

    # Port must be default 443 or None
    if parts.port is not None and parts.port != 443:
        return False, f"Non-standard port {parts.port} prohibited", None, None

    # Domain allowlist check
    if not is_allowed_domain(hostname, ALLOWED_DOMAINS):
        return False, f"Domain {hostname} is not in the allowed social media domains list", None, None

    # DNS resolution & SSRF IP check
    valid_ip, pinned_ip, ip_err = resolve_and_validate_hostname(hostname)
    if not valid_ip:
        return False, ip_err, hostname, None

    return True, "", hostname, pinned_ip


def validate_merchant_redirect_url(url: str) -> Tuple[bool, str]:
    """
    Validates an affiliate merchant redirect URL against scheme, credentials, ports, and allowed merchant domains.
    Prevents open-redirect vulnerabilities.
    """
    if not url or not isinstance(url, str):
        return False, "Redirect URL must be a non-empty string"

    url_str = url.strip()

    try:
        parts = urllib.parse.urlsplit(url_str)
    except Exception as e:
        return False, f"Invalid redirect URL structure: {e}"

    if parts.scheme.lower() != "https":
        return False, "Only HTTPS redirect URLs are allowed"

    if parts.username or parts.password:
        return False, "Redirect URLs containing credentials are prohibited"

    hostname = parts.hostname
    if not hostname:
        return False, "Redirect URL missing valid hostname"
    hostname = hostname.lower()

    if parts.port is not None and parts.port != 443:
        return False, f"Non-standard port {parts.port} prohibited"

    if not is_allowed_domain(hostname, ALLOWED_MERCHANT_DOMAINS):
        return False, f"Merchant domain {hostname} is not in the allowed merchant domains list"

    return True, ""


def validate_url_and_follow_redirects(initial_url: str, max_redirects: int = 3) -> Tuple[bool, str, str]:
    """
    Validates initial URL and follows redirects up to max_redirects hops.
    Re-validates resolved IP and hostname after every redirect hop to block SSRF via open redirectors.
    Returns (is_valid, error_message, final_url).
    """
    current_url = initial_url
    redirect_count = 0

    while redirect_count <= max_redirects:
        is_valid, err_msg, hostname, pinned_ip = validate_social_url(current_url)
        if not is_valid:
            return False, f"URL validation failed at hop {redirect_count}: {err_msg}", current_url

        # Check if HTTP request redirects
        try:
            import urllib.request
            req = urllib.request.Request(current_url, method="HEAD", headers={"User-Agent": "UniversalProAI/1.0"})
            class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
                def redirect_request(self, req, fp, code, msg, headers, newurl):
                    return None # Do not auto-follow
            opener = urllib.request.build_opener(NoRedirectHandler)
            try:
                resp = opener.open(req, timeout=5)
                # No redirect
                return True, "", current_url
            except urllib.error.HTTPError as e:
                if e.code in (301, 302, 303, 307, 308):
                    location = e.headers.get("Location")
                    if not location:
                        return True, "", current_url # No Location header
                    # Resolve relative redirect URLs
                    next_url = urllib.parse.urljoin(current_url, location)
                    redirect_count += 1
                    if redirect_count > max_redirects:
                        return False, f"Maximum redirect count ({max_redirects}) exceeded", current_url
                    current_url = next_url
                else:
                    # Non-redirect status code
                    return True, "", current_url
        except Exception:
            # If HEAD fails or network error, default to initial validation result
            return True, "", current_url

    return True, "", current_url


def generate_stream_token(extraction_id: str, secret_key: str) -> str:
    """Generates a signed HMAC stream token for video stream proxying."""
    if not secret_key:
        secret_key = "universal_pro_default_secret_key"
    key_bytes = secret_key.encode('utf-8')
    msg_bytes = extraction_id.encode('utf-8')
    return hmac.new(key_bytes, msg_bytes, hashlib.sha256).hexdigest()


def verify_stream_token(extraction_id: str, token: str, secret_key: str) -> bool:
    """Verifies a signed HMAC stream token in constant time."""
    if not extraction_id or not token:
        return False
    if not secret_key:
        secret_key = "universal_pro_default_secret_key"
    expected = generate_stream_token(extraction_id, secret_key)
    return hmac.compare_digest(expected, token)

