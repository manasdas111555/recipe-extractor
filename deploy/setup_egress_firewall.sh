#!/usr/bin/env bash
# ==============================================================================
# Universal Pro AI — Production & Staging Host Egress Firewall Setup (UPA-1206)
# Enforces strict outbound network filtering for Docker API and Worker containers
# Blocks cloud metadata (169.254.169.254), link-local, and RFC 1918 private subnets.
#
# Idempotent: can be run repeatedly without duplicating rules.
# Preserves compose-to-compose internal traffic and inbound host traffic.
# ==============================================================================

set -euo pipefail

COMPOSE_SUBNET="${COMPOSE_SUBNET:-172.28.0.0/16}"
DOCKER_BRIDGE_RANGE="172.16.0.0/12"

echo "==> Configuring iptables DOCKER-USER chain egress rules for subnet: ${COMPOSE_SUBNET}..."

# 1. Ensure DOCKER-USER chains exist in iptables and ip6tables
iptables -N DOCKER-USER 2>/dev/null || true
ip6tables -N DOCKER-USER 2>/dev/null || true

# Flush chain first to guarantee idempotency
iptables -F DOCKER-USER
ip6tables -F DOCKER-USER

# 2. Allow established and related connections (fast path)
iptables -A DOCKER-USER -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
ip6tables -A DOCKER-USER -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# 3. Allow internal Compose-to-Compose communication (before private range rejects)
iptables -A DOCKER-USER -s "${COMPOSE_SUBNET}" -d "${COMPOSE_SUBNET}" -j RETURN
iptables -A DOCKER-USER -s "${DOCKER_BRIDGE_RANGE}" -d "${DOCKER_BRIDGE_RANGE}" -j RETURN

# 4. Allow container outbound DNS (UDP/TCP port 53)
iptables -A DOCKER-USER -s "${COMPOSE_SUBNET}" -p udp --dport 53 -j RETURN
iptables -A DOCKER-USER -s "${COMPOSE_SUBNET}" -p tcp --dport 53 -j RETURN
ip6tables -A DOCKER-USER -p udp --dport 53 -j RETURN
ip6tables -A DOCKER-USER -p tcp --dport 53 -j RETURN

# 5. Allow container outbound HTTPS (port 443) for AI APIs, Telegram, WhatsApp, Supabase, Social & Merchant CDNs
iptables -A DOCKER-USER -s "${COMPOSE_SUBNET}" -p tcp --dport 443 -j RETURN
ip6tables -A DOCKER-USER -p tcp --dport 443 -j RETURN

# 6. Allow container outbound Upstash Redis / Celery broker ports (port 6379, 33816)
iptables -A DOCKER-USER -s "${COMPOSE_SUBNET}" -p tcp --dport 6379 -j RETURN
iptables -A DOCKER-USER -s "${COMPOSE_SUBNET}" -p tcp --dport 33816 -j RETURN

# 7. Allow container outbound Supabase Postgres (port 5432, 6543)
iptables -A DOCKER-USER -s "${COMPOSE_SUBNET}" -p tcp --dport 5432 -j RETURN
iptables -A DOCKER-USER -s "${COMPOSE_SUBNET}" -p tcp --dport 6543 -j RETURN

# 8. Explicitly DENY Cloud Instance Metadata Service (169.254.169.254/32 and 169.254.0.0/16)
iptables -A DOCKER-USER -s "${COMPOSE_SUBNET}" -d 169.254.169.254/32 -j REJECT --reject-with icmp-port-unreachable
iptables -A DOCKER-USER -s "${COMPOSE_SUBNET}" -d 169.254.0.0/16 -j REJECT --reject-with icmp-port-unreachable
iptables -A DOCKER-USER -d 169.254.169.254/32 -j REJECT --reject-with icmp-port-unreachable
iptables -A DOCKER-USER -d 169.254.0.0/16 -j REJECT --reject-with icmp-port-unreachable

# 9. Explicitly DENY RFC 1918 Private IPv4 Subnets for Container Outbound Traffic
iptables -A DOCKER-USER -s "${COMPOSE_SUBNET}" -d 10.0.0.0/8 -j REJECT --reject-with icmp-port-unreachable
iptables -A DOCKER-USER -s "${COMPOSE_SUBNET}" -d 172.16.0.0/12 -j REJECT --reject-with icmp-port-unreachable
iptables -A DOCKER-USER -s "${COMPOSE_SUBNET}" -d 192.168.0.0/16 -j REJECT --reject-with icmp-port-unreachable
iptables -A DOCKER-USER -s "${COMPOSE_SUBNET}" -d 127.0.0.0/8 -j REJECT --reject-with icmp-port-unreachable

# 10. IPv6 Private / Unique Local & Link-Local REJECT rules
ip6tables -A DOCKER-USER -d fc00::/7 -j REJECT
ip6tables -A DOCKER-USER -d fe80::/10 -j REJECT
ip6tables -A DOCKER-USER -d ::1/128 -j REJECT

# 11. Default RETURN to allow other standard docker traffic through chain
iptables -A DOCKER-USER -j RETURN
ip6tables -A DOCKER-USER -j RETURN

# 12. Save rules for persistence across host reboots (if tooling installed)
if command -v netfilter-persistent &>/dev/null; then
    netfilter-persistent save 2>/dev/null || true
elif [ -d "/etc/iptables" ]; then
    iptables-save > /etc/iptables/rules.v4 2>/dev/null || true
    ip6tables-save > /etc/iptables/rules.v6 2>/dev/null || true
fi

echo "==> Host egress firewall setup complete. DOCKER-USER chain active and hardened."

