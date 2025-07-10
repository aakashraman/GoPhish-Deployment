#!/usr/bin/env python3

import os
import subprocess
import json
import argparse
import time
import requests

# Constants
GOPHISH_VERSION = "v0.12.1"
GOPHISH_DIR = "/opt/gophish"
LOG_FILE = f"{GOPHISH_DIR}/gophish_setup.log"

# Optional: Add your Namecheap credentials here or export them as ENV vars
NAMECHEAP_API_USER = os.getenv("NAMECHEAP_API_USER", "")
NAMECHEAP_API_KEY = os.getenv("NAMECHEAP_API_KEY", "")

def run_command(cmd, check=True):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, check=check, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.stdout.strip()

def update_system():
    run_command("apt update && apt upgrade -y")
    run_command("apt install unzip certbot -y")

def setup_gophish():
    os.makedirs(GOPHISH_DIR, exist_ok=True)
    os.chdir(GOPHISH_DIR)

    zip_url = f"https://github.com/gophish/gophish/releases/download/{GOPHISH_VERSION}/gophish-{GOPHISH_VERSION}-linux-64bit.zip"
    run_command(f"wget {zip_url}")
    run_command(f"unzip gophish-{GOPHISH_VERSION}-linux-64bit.zip")
    run_command("chmod +x gophish")

def request_ssl_certificate(domain):
    print("Launching Certbot... follow the DNS instructions.")
    run_command(f"certbot certonly -d {domain} --manual --preferred-challenges dns --register-unsafely-without-email")

def modify_config(domain):
    cert_path = f"/etc/letsencrypt/live/{domain}/fullchain.pem"
    key_path = f"/etc/letsencrypt/live/{domain}/privkey.pem"
    config_path = f"{GOPHISH_DIR}/config.json"

    with open(config_path, 'r') as f:
        config = json.load(f)

    config["admin_server"]["listen_url"] = "0.0.0.0:3333"
    config["admin_server"]["use_tls"] = True
    config["admin_server"]["cert_path"] = cert_path
    config["admin_server"]["key_path"] = key_path

    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)

    print("Updated config.json with SSL paths and listen_url.")

def start_gophish():
    os.chdir(GOPHISH_DIR)
    print("Starting GoPhish...")
    with open(LOG_FILE, "w") as log_file:
        subprocess.Popen(["./gophish"], stdout=log_file, stderr=log_file)

def create_namecheap_dns_record(domain, host, value, record_type="TXT"):
    if not NAMECHEAP_API_USER or not NAMECHEAP_API_KEY:
        print("Namecheap API credentials not set. Skipping DNS automation.")
        return

    sld, tld = domain.split(".", 1)
    url = f"https://api.namecheap.com/xml.response"
    payload = {
        "ApiUser": NAMECHEAP_API_USER,
        "ApiKey": NAMECHEAP_API_KEY,
        "UserName": NAMECHEAP_API_USER,
        "ClientIp": "127.0.0.1",  # Optional or replace with external IP
        "Command": "namecheap.domains.dns.setHosts",
        "SLD": sld,
        "TLD": tld,
        "HostName1": host,
        "RecordType1": record_type,
        "Address1": value,
        "TTL1": 60,
    }

    print("Creating DNS record via Namecheap...")
    response = requests.post(url, data=payload)
    print(response.text)

def main():
    parser = argparse.ArgumentParser(description="Deploy GoPhish with SSL and optional DNS setup")
    parser.add_argument('-d', '--domain', required=True, help='Domain name (e.g. example.com)')
    args = parser.parse_args()
    domain = args.domain.strip()

    print(f"\n📦 Deploying GoPhish for domain: {domain}\n")
    update_system()
    setup_gophish()
    request_ssl_certificate(domain)
    modify_config(domain)
    start_gophish()

    print(f"\n✅ GoPhish is now running at: https://{domain}:3333")
    print(f"📜 Logs are stored in: {LOG_FILE}")

if __name__ == "__main__":
    main()
