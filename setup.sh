#!/bin/bash
# Setup script for EV Blog Automation Suite

# Exit on error
set -e

# Function to handle errors
handle_error() {
    echo "Error: $1"
    exit 1
}

echo "Setting up EV Blog Automation Suite..."

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p logs || handle_error "Failed to create logs directory"
mkdir -p images || handle_error "Failed to create images directory"
mkdir -p modules/webdriver || handle_error "Failed to create webdriver directory"

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt || handle_error "Failed to install Python dependencies"

# Install ChromeDriver
echo "Installing ChromeDriver..."
python3 -c "
import os
import sys
import subprocess
from modules.patch import download_lastest_chromedriver, install_ssl_certificates

# Get the current working directory
current_dir = os.getcwd()
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
" || handle_error "Failed to install ChromeDriver or SSL certificates"

# Run setup.py
echo "Running setup.py..."
python3 setup.py || handle_error "Failed to run setup.py"

echo "Setup completed successfully!"
