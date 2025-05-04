#!/bin/bash
# Setup script for EV Blog Automation Suite

echo "Setting up EV Blog Automation Suite..."

# Create necessary directories
mkdir -p logs
mkdir -p images

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Install ChromeDriver
echo "Installing ChromeDriver..."
python3 -c "
import os
import sys
import subprocess
from modules.patch import download_lastest_chromedriver, install_ssl_certificates

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
webdriver_dir = os.path.join(current_dir, 'modules', 'webdriver')

# Create webdriver directory if it doesn't exist
os.makedirs(webdriver_dir, exist_ok=True)

# Download ChromeDriver
if download_lastest_chromedriver():
    print('ChromeDriver installed successfully')
else:
    print('Failed to install ChromeDriver')
    sys.exit(1)

# Install SSL certificates
if install_ssl_certificates():
    print('SSL certificates installed successfully')
else:
    print('Failed to install SSL certificates')
    sys.exit(1)
"

# Run setup.py
echo "Running setup.py..."
python3 setup.py

echo "Setup completed successfully!"
