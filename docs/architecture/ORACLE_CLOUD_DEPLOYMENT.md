# 🚀 Universal Pro AI — Oracle Cloud Infrastructure (OCI) Production Runbook

This document details the complete, end-to-end setup of our dedicated **24/7 Always Free cloud production environment** on **Oracle Cloud Infrastructure (OCI)**, including the architectural topology, setup procedures, and a detailed engineering log of all issues encountered and resolved.

---

## 📌 Production Server Specification
- **Tenancy**: `manasdas111555`
- **Region**: `India South (Hyderabad)` (`ap-hyderabad-1`)
- **Instance Name**: `universal-pro-ai-instance`
- **Public IPv4 Address**: `140.245.214.28` (Permanent Reserved Static IP)
- **Operating System**: `Canonical Ubuntu 24.04 LTS`
- **Compute Shape**: `VM.Standard.E2.1.Micro` (AMD 1-core OCPU, 1 GB RAM + 2 GB Swap Space, Always Free)
- **Virtual Cloud Network**: `universalpro-ai-vcn` (10.0.0.0/16)
- **Subnet**: `public subnet-universalpro-ai-vcn` (10.0.0.0/24)
- **Internet Gateway**: Active (`universalpro-ai-vcn-ig`)
- **Monthly Infrastructure Cost**: **$0.00 / month (100% Free Forever)**

---

## 🏗️ Architecture & Component Topology

```
User Requests (Web, Mobile, WhatsApp, Telegram)
                       │
                       ▼
          Public IP: 140.245.214.28
      ┌─────────────────────────────────┐
      │   Oracle VCN Security List      │
      │   Allowed Ports: 22, 80, 443,   │
      │                  8000           │
      └────────────────┬────────────────┘
                       │
                       ▼
   ┌───────────────────────────────────────────────┐
   │         Ubuntu 24.04 Production VM            │
   │  ┌─────────────────────────────────────────┐  │
   │  │ Caddy Reverse Proxy (Port 80 / 443)     │  │
   │  └────────────────────┬────────────────────┘  │
   │                       │                       │
   │         ┌─────────────┴─────────────┐         │
   │         ▼                           ▼         │
   │  ┌──────────────┐            ┌──────────────┐ │
   │  │ FastAPI API  │            │ Celery Worker│ │
   │  │  (Port 8000) │            │ (Extraction) │ │
   │  └──────┬───────┘            └──────┬───────┘ │
   │         │                           │         │
   │         └─────────────┬─────────────┘         │
   │                       ▼                       │
   │             ┌──────────────────┐              │
   │             │   Redis Server   │              │
   │             │   (Port 6379)    │              │
   │             └──────────────────┘              │
   │                                               │
   │   2GB Virtual Swap File (/swapfile)           │
   └───────────────────────────────────────────────┘
```

---

## 📋 Comprehensive Setup Log & Steps Taken

### Step 1: OCI Account Creation & Verification
1. Registered on `https://www.oracle.com/cloud/free/`.
2. Selected **Account Type**: `Individual`.
3. Selected **Home Region**: `India South (Hyderabad)` (`ap-hyderabad-1`).
4. Completed identity and card verification (temporary ₹75–₹100 pre-authorization charge, immediately refunded).

### Step 2: Virtual Cloud Network (VCN) with Internet Gateway
To ensure instances have internet connectivity and public IP assignment:
1. Navigated to **Networking** $\rightarrow$ **Virtual Cloud Networks**.
2. Launched **Start VCN Wizard** $\rightarrow$ selected **Create VCN with Internet Connectivity**.
3. **VCN Name**: `universalpro-ai-vcn`.
4. Configured IPv4 CIDR Blocks:
   - VCN CIDR: `10.0.0.0/16`
   - Public Subnet CIDR: `10.0.0.0/24`
   - Private Subnet CIDR: `10.0.1.0/24`
5. Verified Internet Gateway, NAT Gateway, and Service Gateway were provisioned.

### Step 3: Firewall & Ingress Rules Configuration
In **Default Security List for universalpro-ai-vcn**, added the following Ingress Rules:
| Stateless | Source CIDR | IP Protocol | Destination Port Range | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| No | `0.0.0.0/0` | TCP | `22` | SSH Remote Login |
| No | `0.0.0.0/0` | TCP | `80` | HTTP Web Traffic |
| No | `0.0.0.0/0` | TCP | `443` | HTTPS Encrypted Web Traffic |
| No | `0.0.0.0/0` | TCP | `8000` | FastAPI Direct API Gateway |

### Step 4: Compute VM Instance Creation
1. **Name**: `universal-pro-ai-instance`
2. **OS Image**: `Canonical Ubuntu 24.04 LTS`
3. **Compute Shape**: `VM.Standard.E2.1.Micro` (Always Free)
4. **Networking**: Selected existing VCN `universalpro-ai-vcn` and `public subnet-universalpro-ai-vcn`.
5. **Public IP**: Assigned automatically (`140.245.214.28`).
6. **SSH Key Pair**: Generated and downloaded private key `ssh-key-2026-09-08.key`.
7. **Boot Volume**: 46.6 GB default SSD.

---

## 🛠️ Issues Encountered & Engineering Resolutions

During the cloud deployment process, several real-world cloud engineering challenges were identified and systematically resolved:

### Issue 1: Hostinger Domain (`mpdtech.in`) Suspended by NIXI Registry
- **Symptom**: Domain `mpdtech.in` showed `Suspended` badge in Hostinger despite being paid until Feb 2027.
- **Root Cause**: The Indian `.IN` Registry (NIXI) flagged the domain for mandatory national KYC audit (requiring Aadhaar/Passport and address proof submission via support tickets).
- **Resolution**: Decoupled infrastructure from the suspended domain. Chose to route traffic directly via Oracle's permanent static public IP (`140.245.214.28`) and Vercel's free global CDN domain, bypassing days of bureaucratic registry delay.

### Issue 2: Image vs Shape Architecture Warning (`aarch64` vs `x86`)
- **Symptom**: Oracle Console displayed warning *"This image has no compatible image builds for the current shape."*
- **Root Cause**: An ARM 64-bit image (`Canonical Ubuntu 24.04 Minimal aarch64`) was selected while the underlying compute shape was configured for x86 (AMD).
- **Resolution**: Switched the operating system image to standard `Canonical Ubuntu 24.04` (x86_64), clearing the warning completely.

### Issue 3: Public IPv4 Toggle Locked in Instance Wizard
- **Symptom**: Toggle for *"Automatically assign public IPv4 address"* was disabled with warning: *"You must select a public subnet to assign a public IPv4 address."*
- **Root Cause**: Creating a VCN inline inside the VM creation wizard fails to attach a default Internet Gateway before the subnet is saved.
- **Resolution**: Launched Oracle's standalone **VCN Wizard** with *"Create VCN with Internet Connectivity"*. Once the VCN was created with an attached Internet Gateway, the VM wizard immediately recognized the public subnet and enabled the public IP toggle.

### Issue 4: Ampere A1 Compute Host Out-of-Capacity
- **Symptom**: `API Error: Out of capacity for shape VM.Standard.A1.Flex in availability domain AD-1.`
- **Root Cause**: Oracle's Hyderabad data center (`ap-hyderabad-1`) had high demand on 4-core ARM physical hardware.
- **Resolution**: Selected the AMD Always Free shape (`VM.Standard.E2.1.Micro`). To compensate for the 1 GB physical memory, we configured a **2 GB Linux Swap file** (`/swapfile`), providing 3 GB total effective memory—more than enough for FastAPI, Celery, and Redis.

### Issue 5: Oracle API Rate Limiter
- **Symptom**: `API Error: Too many requests for the user.`
- **Root Cause**: Triggered by multiple quick clicks on the instance creation button after the capacity error.
- **Resolution**: Implemented a mandatory 60-second cooldown period before re-submitting. The subsequent request succeeded immediately.

### Issue 6: Windows OpenSSH "Bad Permissions: Key Is Too Open"
- **Symptom**: When running `ssh -i ssh-key-2026-09-08.key ubuntu@140.245.214.28`, Windows OpenSSH rejected the key with:
  ```
  WARNING: UNPROTECTED PRIVATE KEY FILE!
  Permissions for 'ssh-key-2026-09-08.key' are too open.
  Load key: bad permissions
  Permission denied (publickey).
  ```
- **Root Cause**: Windows NTFS inherits permissions allowing `NT AUTHORITY\Authenticated Users` and `BUILTIN\Users` to read files in the directory. OpenSSH mandates that private keys be strictly accessible ONLY by the current user.
- **Resolution**: Executed Windows `icacls` to disable inheritance and strip all unauthorized group access:
  ```powershell
  icacls "ssh-key-2026-09-08.key" /inheritance:r
  icacls "ssh-key-2026-09-08.key" /grant:r "$($env:USERNAME):(R)"
  icacls "ssh-key-2026-09-08.key" /remove "NT AUTHORITY\Authenticated Users"
  icacls "ssh-key-2026-09-08.key" /remove "BUILTIN\Users"
  icacls "ssh-key-2026-09-08.key" /remove "BUILTIN\Administrators"
  ```
  SSH connection succeeded immediately on the next attempt.

### Issue 7: SSH Connection Reset Silently Drops to Local PowerShell
- **Symptom**: During interactive bash `.env` creation on the server, the SSH socket reset (`client_loop: send disconnect: Connection reset`), dropping the prompt back to local Windows PowerShell (`PS D:\...`). Pasting bash multi-line commands into PowerShell produced redirection syntax errors.
- **Root Cause**: Transient socket timeout between client and cloud VM, combined with syntax differences between POSIX bash and Windows PowerShell.
- **Resolution**: Used automated `scp` with the private key to transfer `.env` directly from the local workspace to `~/recipe-extractor/.env` on the server in 2 seconds, eliminating interactive typing hazards.

### Issue 8: Python 3.11 Runtime `NameError: name 'Any' is not defined`
- **Symptom**: `universalpro-api` crashed repeatedly on container boot with `NameError: name 'Any' is not defined` in `backend/app/services/quota_service.py:135`.
- **Root Cause**: Missing `Any` from `typing` module imports (`from typing import Tuple, Dict, Optional`). Evaluated eagerly during class loading in Python 3.11 inside Docker.
- **Resolution**: Added `Any` to `backend/app/services/quota_service.py`, committed to git, ran `git pull origin main` on the server, and rebuilt the API and worker containers via `docker compose up -d --build api worker`.

---

## 💻 Server Bootstrap & Docker Deployment

### 1. Execute Server Preparation Script
Run inside the Ubuntu SSH terminal (`ubuntu@universal-pro-ai-vnic:~$`):

```bash
# 1. Update system packages
sudo apt update && sudo apt upgrade -y

# 2. Install official Docker & Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# 3. Provision 2GB Virtual Swap Space
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# 4. Open Ubuntu OS internal firewall
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 8000 -j ACCEPT
sudo apt install -y iptables-persistent
sudo netfilter-persistent save

# 5. Switch to docker group
newgrp docker
```

### 2. Deploy Repository Stack
```bash
# Clone the repository
git clone https://github.com/manasdas111555/recipe-extractor.git
cd recipe-extractor

# Configure environment secrets
nano .env
# (Save Supabase, Gemini, and monetization keys)

# Start multi-container stack
docker compose up -d --build
```

---

## 🔍 Health Checks & Validation

Once the containers are running:
```bash
# Verify containers status
docker compose ps

# Test local health endpoint
curl http://localhost/health
# Response: {"status":"healthy"}
```

Access from any web browser:
- **Health Check**: `http://140.245.214.28/health`
- **Swagger Interactive API Docs**: `http://140.245.214.28/docs`

---

## 🌐 Layer 7 Shield & Global CDN: Vercel Edge Frontend

To protect the Oracle Cloud raw IP from DDoS attacks, scraping, and brute force attempts, we placed a **Vercel Edge Next.js 15 PWA frontend** in front of the Oracle Cloud VM:

```
End Users (Global Browsers, Mobile PWAs)
                     │
                     ▼ HTTPS (Let's Encrypt / Vercel Edge Network)
      https://universal-pro-ai.vercel.app
                     │
         [Next.js Dynamic Rewrites]
         /api/:path* ──► http://140.245.214.28/api/:path*
                     │
                     ▼
          Oracle Cloud OCI Backend (Hyderabad)
         (Shielded, Always-Free, 24/7 Compute)
```

### Benefits of this Architecture:
1. **100% Free HTTPS & SSL**: Vercel handles automated TLS termination with zero certificate renewals needed.
2. **Origin IP Shielding**: End users only see and interact with `https://universal-pro-ai.vercel.app`. The Oracle Cloud IP address is never directly exposed in user address bars.
3. **Global Edge Caching**: Assets, images, and static routes are distributed across worldwide edge locations, achieving sub-second first-paint response times.
4. **$0.00 Total Cost**: 100% Free on Vercel Hobby + 100% Free on Oracle Cloud Always Free.

