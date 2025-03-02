#!/bin/bash

# Update system
apt-get update
apt-get upgrade -y

# Install required packages
apt-get install -y curl

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama
systemctl start ollama

# Pull the llama2 model
ollama pull llama2

# Install Nginx
apt-get install -y nginx

# Create Nginx configuration
cat > /etc/nginx/sites-available/ollama << 'EOL'
server {
    listen 80;
    server_name your_server_ip;

    location / {
        proxy_pass http://localhost:11434;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOL

# Enable the site
ln -s /etc/nginx/sites-available/ollama /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default

# Test and restart Nginx
nginx -t
systemctl restart nginx

# Install UFW firewall and configure it
apt-get install -y ufw
ufw allow ssh
ufw allow http
ufw allow https
ufw --force enable
