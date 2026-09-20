#!/usr/bin/env bash
# ==============================================================================
# Universal Pro AI — Production & Staging Host Egress Firewall Setup
# Enforces strict outbound network filtering for Docker API and Worker containers
# Blocks cloud metadata (169.254.169.254), link-local, and private subnets.
# ==============================================================================

set -euo pipefail

echo "==> Configuring iptables DOCKER-USER chain egress rules..."

# Ensure DOCKER-USER chain exists
iptables -N DOCKER-USER 2>/dev/null || true

# 1. Allow established and related connections
iptables -A DOCKER-USER -m state --state ESTABLISHED,RELATED -j ACCEPT

# 2. Allow outbound DNS (port 53 UDP/TCP)
iptables -A DOCKER-USER -p udp --dport 53 -j ACCEPT
iptables -A DOCKER-USER -p tcp --dport 53 -j ACCEPT

# 3. Allow internal Docker bridge communication (subnet 172.18.0.0/16 or standard 172.17.0.0/16)
# Adjust subnet if custom docker-compose network is configured
iptables -A DOCKER-USER -s 172.16.0.0/12 -d 172.16.0.0/12 -j ACCEPT

# 4. Explicitly DENY Cloud Instance Metadata Service (169.254.169.254)
iptables -A DOCKER-USER -d 169.254.169.254/32 -j REJECT --reject-with icmp-port-unreachable
iptables -A DOCKER-USER -d 169.254.0.0/16 -j REJECT --reject-with icmp-port-unreachable

# 5. Explicitly DENY Private IPv4 Subnets (RFC 1918) for Outbound Traffic
iptables -A DOCKER-USER -d 10.0.0.0/8 -j REJECT --reject-with icmp-port-unreachable
iptables -A DOCKER-USER -d 192.168.0.0/16 -j REJECT --reject-with icmp-port-unreachable
iptables -A DOCKER-USER -d 127.0.0.0/8 -j REJECT --reject-with icmp-port-unreachable

# 6. Allow outbound HTTPS (port 443) for AI APIs, Telegram, WhatsApp, Supabase, Merchant & Social hosts
iptables -A DOCKER-USER -p tcp --dport 443 -j ACCEPT

# 7. Allow outbound Rediss / Celery Broker ports (port 6379, 33816)
iptables -A DOCKER-USER -p tcp --dport 6379 -j ACCEPT
iptables -A DOCKER-USER -p tcp --dport 33816 -j ACCEPT

# 8. Allow outbound Supabase Postgres (port 5432, 6543)
iptables -A DOCKER-USER -p tcp --dport 5432 -j ACCEPT
iptables -A DOCKER-USER -p tcp --dport 6543 -j ACCEPT

# 9. Default RETURN to allow other standard docker traffic through chain
iptables -A DOCKER-USER -j RETURN

echo "==> Host egress firewall setup complete."
