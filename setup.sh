#!/bin/bash
# Setup script for EV Blog Automation Suite

echo "Setting up EV Blog Automation Suite..."

# Create necessary directories
mkdir -p logs
mkdir -p temp/images
mkdir -p modules/webdriver

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install ChromeDriver
echo "Installing ChromeDriver..."
CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d'.' -f1)
CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION")
OS_TYPE=$(uname -s)

if [ "$OS_TYPE" = "Darwin" ]; then
    # macOS
    curl -L "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_mac64.zip" -o chromedriver.zip
    unzip chromedriver.zip -d modules/webdriver/
    rm chromedriver.zip
    chmod +x modules/webdriver/chromedriver
elif [ "$OS_TYPE" = "Linux" ]; then
    # Linux
    curl -L "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip" -o chromedriver.zip
    unzip chromedriver.zip -d modules/webdriver/
    rm chromedriver.zip
    chmod +x modules/webdriver/chromedriver
else
    echo "Unsupported operating system: $OS_TYPE"
    exit 1
fi

# Install SSL certificates for Python
echo "Installing SSL certificates..."
if [ "$OS_TYPE" = "Darwin" ]; then
    # macOS
    /Applications/Python\ 3.*/Install\ Certificates.command
fi

# Run the setup.py script
echo "Running setup script..."
python3 setup.py

echo "Setup complete! You can now run the web interface with:"
echo "python3 run_web_interface.py"
