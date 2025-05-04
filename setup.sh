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
if [ "$(uname)" == "Darwin" ]; then
    # macOS
    CHROME_VERSION=$(/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version | awk '{print $3}' | cut -d'.' -f1)
    echo "Detected Chrome version: $CHROME_VERSION"
    
    # Download ChromeDriver
    echo "Downloading ChromeDriver..."
    curl -L "https://storage.googleapis.com/chrome-for-testing-public/$CHROME_VERSION/mac-x64/chromedriver-mac-x64.zip" -o chromedriver.zip
    
    # Extract and move to correct location
    unzip -o chromedriver.zip -d modules/webdriver/
    mv modules/webdriver/chromedriver-mac-x64/chromedriver modules/webdriver/
    rm -rf modules/webdriver/chromedriver-mac-x64
    rm chromedriver.zip
    
    # Make executable
    chmod +x modules/webdriver/chromedriver
    echo "ChromeDriver installed successfully"
else
    echo "Unsupported operating system"
    exit 1
fi

# Install SSL certificates for Python
echo "Installing SSL certificates..."
if [ "$(uname)" == "Darwin" ]; then
    # macOS
    /Applications/Python\ 3.*/Install\ Certificates.command
fi

# Run the setup.py script
echo "Running setup script..."
python3 setup.py

echo "Setup complete! You can now run the web interface with:"
echo "python3 run_web_interface.py"
