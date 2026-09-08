# 🚀 Oracle Cloud Always Free Production Deployment Guide

## Server Details
- **Public IP**: `140.245.214.28`
- **Default Username**: `ubuntu`
- **OS**: Ubuntu 24.04 LTS (AMD Always Free)

---

## 1. Connecting to the Server via SSH

From your local machine (PowerShell or Terminal):

```bash
ssh -i "path/to/your-ssh-key.key" ubuntu@140.245.214.28
```

*(If you get a `Permissions are too open` warning on the key file on Windows, move it to `~/.ssh/` or run `icacls "your-key.key" /inheritance:r /grant:r "%USERNAME%:R"`).*

---

## 2. One-Time Server Setup Script (Run on Ubuntu Server)

Once logged into your server, copy and paste this command block:

```bash
# 1. Update packages
sudo apt update && sudo apt upgrade -y

# 2. Add 2GB Swap Memory (guarantees zero OOM crashes)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# 3. Install Docker & Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# 4. Open Ubuntu OS Firewall for Web Ports
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 8000 -j ACCEPT
sudo netfilter-persistent save 2>/dev/null || sudo apt install -y iptables-persistent && sudo netfilter-persistent save

# Apply docker group without logout
newgrp docker
```

---

## 3. Clone Repository & Run Docker Stack

```bash
# Clone the repository
git clone https://github.com/manasdas111555/recipe-extractor.git
cd recipe-extractor

# Create your .env file with your production secrets
nano .env
# (Paste your SUPABASE_URL, SUPABASE_KEY, GEMINI_API_KEY, JWT_SECRET, etc., then press Ctrl+O, Enter, Ctrl+X)

# Launch all containers in background
docker compose up -d --build
```

---

## 4. Verify Services

Check running containers:
```bash
docker compose ps
```

Test the live endpoint:
```bash
curl http://localhost/health
# Response: {"status":"healthy"}
```

From your local computer browser:
```
http://140.245.214.28/health
http://140.245.214.28/docs
```
