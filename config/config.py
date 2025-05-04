import os
import logging
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
TEMP_DIR = BASE_DIR / 'temp'
IMAGES_DIR = TEMP_DIR / 'images'
LOGS_DIR = BASE_DIR / 'logs'

# Create necessary directories
TEMP_DIR.mkdir(exist_ok=True)
IMAGES_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Google Sheets Configuration
GOOGLE_SHEETS_CREDENTIALS_PATH = BASE_DIR / 'credentials.json'
SPREADSHEET_ID = ''  # Will be set from web interface
WORKSHEET_NAME = 'Blog Posts'

# WordPress Configuration
WORDPRESS_URL = ''  # Will be set from web interface
WORDPRESS_USERNAME = ''  # Will be set from web interface
WORDPRESS_PASSWORD = ''  # Will be set from web interface

# LLM Configuration
OLLAMA_URL = 'http://localhost:11434'
MODEL_NAME = 'gemma3:latest'

# Image Configuration
MAX_IMAGES_PER_POST = 3  # Will be configurable from web interface
IMAGE_SEARCH_TIMEOUT = 30
IMAGE_DOWNLOAD_TIMEOUT = 30
IMAGE_MIN_WIDTH = 800
IMAGE_MIN_HEIGHT = 600
IMAGE_DOWNLOAD_PATH = IMAGES_DIR
ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp']
DEFAULT_IMAGE_PATH = 'assets/default_images'  # Fallback directory for default images

# Logging Configuration
LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = LOGS_DIR / 'blog_automation.log'

# Content Configuration
ARTICLE_LENGTH = 1000  # Will be configurable from web interface
MAX_RETRIES = 3
RETRY_DELAY = 5

# Google AdSense Configuration
ADSENSE_CLIENT_ID = ''  # Optional: Will be set from web interface if provided
ADSENSE_SLOT_ID = ''  # Optional: Will be set from web interface if provided

# Content Configuration
REQUIRED_ELEMENTS = {
    'table': '<table>',
    'bullet_points': '<ul>',
    'image_slider': '<div class="image-slider">',
    'code_block': '<pre><code>'
}

# Google AdSense Configuration
ADSENSE_SCRIPT = """
<div class="adsense-container">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4921107726870735"
         crossorigin="anonymous"></script>
    <!-- new ad 15 apr -->
    <ins class="adsbygoogle"
         style="display:block"
         data-ad-client="ca-pub-4921107726870735"
         data-ad-slot="6937559389"
         data-ad-format="auto"
         data-full-width-responsive="true"></ins>
    <script>
         (adsbygoogle = window.adsbygoogle || []).push({});
    </script>
</div>
"""