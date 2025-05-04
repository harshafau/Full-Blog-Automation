# -*- coding: utf-8 -*-
"""
Created on Sun May 23 14:44:43 2021

@author: Yicong
"""
#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException, SessionNotCreatedException
import sys
import os
import urllib.request
import ssl
import re
import zipfile
import stat
import json
import shutil
from sys import platform
import logging
import subprocess
import requests
import io
import certifi
import urllib3
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def webdriver_executable():
    if platform == "linux" or platform == "linux2" or platform == "darwin":
        return 'chromedriver'
    return 'chromedriver.exe'

def get_chrome_version():
    """Get the installed Chrome version"""
    try:
        if platform.system() == "Darwin":  # macOS
            # Try different possible Chrome paths on macOS
            chrome_paths = [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "/Applications/Google Chrome Beta.app/Contents/MacOS/Google Chrome Beta",
                "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary"
            ]
            
            for path in chrome_paths:
                if os.path.exists(path):
                    version = subprocess.check_output([path, "--version"]).decode('utf-8')
                    return version.split()[2]  # Returns version number
                    
            logger.error("Chrome not found in standard locations")
            return None
            
        elif platform.system() == "Windows":
            # Windows implementation
            pass
        elif platform.system() == "Linux":
            # Linux implementation
            pass
    except Exception as e:
        logger.error(f"Error getting Chrome version: {str(e)}")
        return None

def download_lastest_chromedriver():
    """Download the latest ChromeDriver version"""
    try:
        # Get Chrome version
        chrome_version = get_chrome_version()
        if not chrome_version:
            logger.error("Could not determine Chrome version")
            return False
            
        # Get major version number
        major_version = chrome_version.split('.')[0]
        
        # Create webdriver directory if it doesn't exist
        current_dir = os.path.dirname(os.path.abspath(__file__))
        webdriver_dir = os.path.join(current_dir, 'webdriver')
        os.makedirs(webdriver_dir, exist_ok=True)
        
        # Download ChromeDriver
        base_url = "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing"
        version_url = f"{base_url}/{chrome_version}/mac-x64/chromedriver-mac-x64.zip"
        
        logger.info(f"Downloading ChromeDriver version {chrome_version}...")
        
        # Create SSL context with certifi
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        
        response = http.request('GET', version_url)
        if response.status != 200:
            logger.error(f"Failed to download ChromeDriver. Status code: {response.status}")
            return False
            
        # Extract the zip file
        with zipfile.ZipFile(io.BytesIO(response.data)) as zip_file:
            # Extract chromedriver
            for file in zip_file.namelist():
                if 'chromedriver' in file and not file.endswith('/'):
                    zip_file.extract(file, webdriver_dir)
                    # Rename the extracted file to 'chromedriver'
                    extracted_path = os.path.join(webdriver_dir, file)
                    target_path = os.path.join(webdriver_dir, 'chromedriver')
                    if os.path.exists(target_path):
                        os.remove(target_path)
                    os.rename(extracted_path, target_path)
                    break
        
        # Make chromedriver executable
        chromedriver_path = os.path.join(webdriver_dir, 'chromedriver')
        os.chmod(chromedriver_path, 0o755)
        
        # Test ChromeDriver
        try:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            service = Service(chromedriver_path)
            driver = webdriver.Chrome(service=service, options=options)
            driver.quit()
            logger.info("ChromeDriver test successful")
        except Exception as e:
            logger.error(f"ChromeDriver test failed: {str(e)}")
            return False
            
        logger.info("ChromeDriver downloaded and installed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error downloading ChromeDriver: {str(e)}")
        return False

def install_ssl_certificates():
    """Install SSL certificates for Python"""
    try:
        # Create SSL context with certifi
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        
        # Test SSL connection
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        response = http.request('GET', 'https://www.google.com')
        
        if response.status == 200:
            logger.info("SSL certificates installed successfully")
            return True
        else:
            logger.error(f"SSL test failed. Status code: {response.status}")
            return False
            
    except Exception as e:
        logger.error(f"Error installing SSL certificates: {str(e)}")
        return False