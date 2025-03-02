# Ollama Server Setup

This guide explains how to set up a dedicated Ollama server for your Tech News website.

## Server Requirements
- Ubuntu 20.04 or later
- Minimum 4GB RAM
- 20GB storage

## Setup Steps

1. Create a DigitalOcean droplet:
   - Choose Ubuntu 22.04 LTS
   - Select Basic plan with 4GB RAM / 2 CPUs
   - Choose a datacenter region close to your users
   - Add your SSH key for secure access

2. Once the droplet is created, note down its IP address

3. SSH into your server:
   ```bash
   ssh root@your_server_ip
   ```

4. Upload the setup script:
   ```bash
   scp setup.sh root@your_server_ip:/root/
   ```

5. Make the script executable and run it:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

6. Update your environment variables:
   - Local development: Add to `.env`:
     ```
     OLLAMA_ENDPOINT=http://your_server_ip/api/generate
     ```
   - Vercel: Add environment variable:
     ```
     OLLAMA_ENDPOINT=http://your_server_ip/api/generate
     ```

## Security Notes
- The server is configured with UFW firewall allowing only SSH and HTTP/HTTPS
- Consider setting up SSL with Let's Encrypt for HTTPS
- Regularly update the system and monitor logs

## Maintenance
- Monitor server resources using:
  ```bash
  htop
  df -h
  ```
- Check Ollama logs:
  ```bash
  journalctl -u ollama
  ```
- Check Nginx logs:
  ```bash
  tail -f /var/log/nginx/access.log
  tail -f /var/log/nginx/error.log
  ```
