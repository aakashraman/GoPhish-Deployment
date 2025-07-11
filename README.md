# GoPhish Auto Deploy Script (DigitalOcean + NameCheap Domain Registrar Combination)

This script automates the deployment of [GoPhish](https://github.com/gophish/gophish), a powerful open-source phishing framework. It supports SSL certificate generation with Let's Encrypt (Certbot) and optionally integrates with the Namecheap API for DNS automation.

---

## Features

- Installs required system packages (`unzip`, `certbot`)
- Downloads and extracts the latest GoPhish release
- Configures `config.json` with:
  - External admin access on `0.0.0.0:3333`
  - SSL certificate and key paths
- Generates SSL certificates via Certbot using DNS challenge
- (Optional) Automates Namecheap DNS TXT record creation
- Launches the GoPhish binary and logs output

---

## Prerequisites

- Ubuntu-based Linux server (e.g., DigitalOcean Droplet)
- A domain name pointed to your server’s IP (via A record)
- Certbot (installed automatically)
- Python 3.6+

---

## Installation & Usage

Clone this repository or download the script directly:

```bash
git clone https://github.com/yourusername/gophish-auto-deploy.git
cd gophish-auto-deploy
```

Basic Usage:

```bash
sudo python3 deploy_gophish.py -d yourdomain.com
```

- Replace yourdomain.com with your actual domain (e.g., hacksmarter-manufacturing.online)

## Optional Tip

If you want the script to automatically create the TXT DNS record (instead of doing it manually), export your Namecheap credentials as environment variables:

```bash
export NAMECHEAP_API_USER="your_namecheap_username"
export NAMECHEAP_API_KEY="your_api_key"
```
✅ Make sure your server’s public IP is whitelisted in your Namecheap API Access Settings

Then run the deployment script again:

```bash
sudo python3 deploy_gophish.py -d yourdomain.com
```
## Final Outcomes 

The script will:

- ✅ Update and upgrade your system
- 📦 Install necessary packages
- 📥 Download and extract GoPhish
- 🔐 Prompt you to complete a DNS TXT challenge using Certbot
- ⚙️ Modify the `config.json` file with your SSL paths
- 🚀 Start GoPhish on `https://yourdomain.com:3333`

## Inspired By:

Course: [Hands-On Phishing](https://academy.simplycyber.io/l/pdp/hands-on-phishing)
Author: [Tyler Rambsbey](https://www.linkedin.com/in/tyler-ramsbey-86221643/)

