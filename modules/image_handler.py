import os
import time
import logging
import requests
from PIL import Image
from io import BytesIO
from config.config import (
    DEFAULT_IMAGE_PATH,
    IMAGE_DOWNLOAD_PATH
)
import sys
# Add the parent directory of the current file to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from .GoogleImageScraper import GoogleImageScraper

class ImageHandler:
    def __init__(self, temp_dir=IMAGE_DOWNLOAD_PATH):
        self.temp_dir = temp_dir
        self.default_dir = DEFAULT_IMAGE_PATH
        self.logger = logging.getLogger(__name__)
        os.makedirs(temp_dir, exist_ok=True)
        os.makedirs(DEFAULT_IMAGE_PATH, exist_ok=True)
        
        # Initialize Google Image Scraper with absolute path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.webdriver_path = os.path.join(current_dir, 'webdriver', 'chromedriver')
        
        # Check if ChromeDriver exists and is executable
        if not os.path.exists(self.webdriver_path):
            self.logger.error("ChromeDriver not found at: %s", self.webdriver_path)
            # Try to download ChromeDriver
            from .patch import download_lastest_chromedriver
            if download_lastest_chromedriver():
                self.logger.info("Successfully downloaded ChromeDriver")
                # Update webdriver path after download
                self.webdriver_path = os.path.join(current_dir, 'webdriver', 'chromedriver')
            else:
                self.logger.error("Failed to download ChromeDriver")
                self.webdriver_path = None
        else:
            # Make sure ChromeDriver is executable
            try:
                os.chmod(self.webdriver_path, 0o755)
                self.logger.info("ChromeDriver found and made executable at: %s", self.webdriver_path)
                
                # Test ChromeDriver
                try:
                    from selenium import webdriver
                    from selenium.webdriver.chrome.service import Service
                    from selenium.webdriver.chrome.options import Options
                    
                    options = Options()
                    options.add_argument('--headless')
                    options.add_argument('--no-sandbox')
                    options.add_argument('--disable-dev-shm-usage')
                    
                    service = Service(self.webdriver_path)
                    driver = webdriver.Chrome(service=service, options=options)
                    driver.quit()
                    self.logger.info("ChromeDriver test successful")
                except Exception as e:
                    self.logger.error("ChromeDriver test failed: %s", str(e))
                    self.webdriver_path = None
                    
            except Exception as e:
                self.logger.error("Failed to make ChromeDriver executable: %s", str(e))
                self.webdriver_path = None

    def search_google_images(self, search_query, num_images=5):
        """Search images using Google Image Scraper"""
        if not self.webdriver_path:
            self.logger.warning("ChromeDriver not available, skipping Google Images search")
            return []
            
        try:
            # Create a new scraper instance for each search
            google_scraper = GoogleImageScraper(
                webdriver_path=self.webdriver_path,
                image_path=self.temp_dir,
                search_key=search_query,
                number_of_images=num_images,
                headless=True,
                min_resolution=(0, 0),  # Accept any resolution
                max_resolution=(3840, 2160)  # Up to 4K resolution
            )
            
            image_urls = google_scraper.find_image_urls()
            if not image_urls:
                self.logger.warning("No images found for query: %s", search_query)
                return []
                
            # Save images and get their paths
            google_scraper.save_images(image_urls, keep_filenames=False)
            
            # Get the saved image paths
            search_dir = os.path.join(self.temp_dir, search_query)
            if not os.path.exists(search_dir):
                self.logger.warning("Search directory not found: %s", search_dir)
                return []
                
            # Accept all image files
            image_paths = [os.path.join(search_dir, f) 
                         for f in os.listdir(search_dir)
                         if os.path.isfile(os.path.join(search_dir, f))]
            
            if not image_paths:
                self.logger.warning("No images saved for query: %s", search_query)
                return []
                
            return image_paths
                   
        except Exception as e:
            self.logger.error(f"Error in Google image search: {str(e)}")
            return []

    def search_and_download_images(self, topic, keywords, num_images=5):
        """Search and download images using Google Image Scraper"""
        try:
            search_query = f"{topic} {keywords}"
            self.logger.info(f"Searching for images with query: {search_query}")

            # Search for images using Google Image Scraper
            image_paths = self.search_google_images(search_query, num_images)
            
            if not image_paths:
                self.logger.warning("No images found from Google Images")
                return []

            return image_paths

        except Exception as e:
            self.logger.error(f"Error in image search: {str(e)}")
            return []

    def select_featured_image(self, images):
        """Select the most suitable image as featured image"""
        if not images:
            return None
        
        # For now, just return the first image
        # In a more sophisticated implementation, you could analyze images
        # to select the most suitable one based on size, aspect ratio, etc.
        return images[0]

    def cleanup(self):
        """Clean up resources"""
        try:
            # Clean up temporary files
            for file in os.listdir(self.temp_dir):
                file_path = os.path.join(self.temp_dir, file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    self.logger.error(f"Error deleting file {file_path}: {str(e)}")
        except Exception as e:
            self.logger.error(f"Error in cleanup: {str(e)}")

    def __del__(self):
        """Destructor to ensure cleanup"""
        self.cleanup() 