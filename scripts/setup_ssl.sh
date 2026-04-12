#!/bin/bash
set -e

# Directory for certs
mkdir -p nginx/certs

# Generate self-signed certificate
echo "Generating self-signed SSL certificate for sslip.io..."
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout nginx/certs/privkey.pem \
    -out nginx/certs/fullchain.pem \
    -subj "/C=US/ST=State/L=City/O=RemoteHustle/CN=*.sslip.io"

echo "SSL certificates generated in nginx/certs/"
