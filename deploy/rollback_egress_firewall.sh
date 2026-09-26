#!/usr/bin/env bash
# ==============================================================================
# Universal Pro AI — Emergency Egress Firewall Rollback Script (UPA-1206)
# Immediately flushes all DOCKER-USER egress firewall rules and restores default RETURN.
# ==============================================================================

set -euo pipefail

echo "==> Rolling back DOCKER-USER iptables and ip6tables chains to default passthrough..."

# Flush IPv4 and IPv6 DOCKER-USER chains
iptables -F DOCKER-USER 2>/dev/null || true
iptables -A DOCKER-USER -j RETURN 2>/dev/null || true

ip6tables -F DOCKER-USER 2>/dev/null || true
ip6tables -A DOCKER-USER -j RETURN 2>/dev/null || true

# Persist rollback state if persistence tooling exists
if command -v netfilter-persistent &>/dev/null; then
    netfilter-persistent save 2>/dev/null || true
elif [ -d "/etc/iptables" ]; then
    iptables-save > /etc/iptables/rules.v4 2>/dev/null || true
    ip6tables-save > /etc/iptables/rules.v6 2>/dev/null || true
fi

echo "==> Rollback complete: DOCKER-USER rules flushed and set to RETURN."
