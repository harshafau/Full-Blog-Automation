# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 13:01:02 2020

@author: OHyic
"""
#import selenium drivers
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

#import helper libraries
import time
import urllib.request
from urllib.parse import urlparse
import os
import requests
import io
from PIL import Image
import re
import logging

#custom patch libraries
from . import patch

class GoogleImageScraper():
    def __init__(self, webdriver_path, image_path, search_key="cat", number_of_images=1, headless=True, min_resolution=(0, 0), max_resolution=(1920, 1080), max_missed=10):
        self.logger = logging.getLogger(__name__)
        
        #check parameter types
        image_path = os.path.join(image_path, search_key)
        if (type(number_of_images)!=int):
            self.logger.error("Number of images must be integer value.")
            return
        if not os.path.exists(image_path):
            self.logger.info("Image path not found. Creating a new folder.")
            os.makedirs(image_path)
            
        #check if chromedriver is installed and executable
        if not os.path.exists(webdriver_path):
            self.logger.error(f"ChromeDriver not found at: {webdriver_path}")
            is_patched = patch.download_lastest_chromedriver()
            if not is_patched:
                self.logger.error("Failed to download ChromeDriver")
                raise Exception("ChromeDriver not found and download failed")
        else:
            try:
                # Make sure ChromeDriver is executable
                os.chmod(webdriver_path, 0o755)
                self.logger.info(f"ChromeDriver found and made executable at: {webdriver_path}")
            except Exception as e:
                self.logger.error(f"Failed to make ChromeDriver executable: {str(e)}")
                raise

        for i in range(3):  # Try up to 3 times
            try:
                #try going to www.google.com
                options = Options()
                if(headless):
                    options.add_argument('--headless')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                service = Service(webdriver_path)
                driver = webdriver.Chrome(service=service, options=options)
                driver.set_window_size(1400,1050)
                driver.get("https://www.google.com")
                try:
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "W0wltc"))).click()
                except Exception as e:
                    self.logger.warning(f"Failed to click accept button: {str(e)}")
                    continue
                break
            except Exception as e:
                self.logger.error(f"Failed to initialize ChromeDriver (attempt {i+1}/3): {str(e)}")
                if i == 2:  # Last attempt
                    raise
                time.sleep(2)  # Wait before retrying

        self.driver = driver
        self.search_key = search_key
        self.number_of_images = number_of_images
        self.webdriver_path = webdriver_path
        self.image_path = image_path
        self.url = "https://www.google.com/search?q=%s&source=lnms&tbm=isch&sa=X&ved=2ahUKEwie44_AnqLpAhUhBWMBHUFGD90Q_AUoAXoECBUQAw&biw=1920&bih=947"%(search_key)
        self.headless=headless
        self.min_resolution = min_resolution
        self.max_resolution = max_resolution
        self.max_missed = max_missed

    def find_image_urls(self):
        """
            This function search and return a list of image urls based on the search key.
            Example:
                google_image_scraper = GoogleImageScraper("webdriver_path","image_path","search_key",number_of_photos)
                image_urls = google_image_scraper.find_image_urls()

        """
        print("[INFO] Gathering image links")
        self.driver.get(self.url)
        image_urls=[]
        count = 0
        missed_count = 0
        indx_1 = 0
        indx_2 = 0
        search_string = '//*[@id="rso"]/div/div/div[1]/div/div/div[%s]/div[2]/h3/a/div/div/div/g-img'
        time.sleep(3)
        while self.number_of_images > count and missed_count < self.max_missed:
            if indx_2 > 0:
                try:
                    imgurl = self.driver.find_element(By.XPATH, search_string%(indx_1,indx_2+1))
                    imgurl.click()
                    indx_2 = indx_2 + 1
                    missed_count = 0
                except Exception:
                    try:
                        imgurl = self.driver.find_element(By.XPATH, search_string%(indx_1+1,1))
                        imgurl.click()
                        indx_2 = 1
                        indx_1 = indx_1 + 1
                    except:
                        indx_2 = indx_2 + 1
                        missed_count = missed_count + 1
            else:
                try:
                    imgurl = self.driver.find_element(By.XPATH, search_string%(indx_1+1))
                    imgurl.click()
                    missed_count = 0
                    indx_1 = indx_1 + 1    
                except Exception:
                    try:
                        imgurl = self.driver.find_element(By.XPATH, search_string%(indx_1,indx_2+1))
                        imgurl.click()
                        missed_count = 0
                        indx_2 = indx_2 + 1
                    except Exception:
                        indx_1 = indx_1 + 1
                        missed_count = missed_count + 1
                    
            try:
                #select image from the popup
                time.sleep(1)
                class_names = ["n3VNCb","iPVvYb","r48jcc","pT0Scc","H8Rx8c"]
                images = [self.driver.find_elements(By.CLASS_NAME, class_name) for class_name in class_names if len(self.driver.find_elements(By.CLASS_NAME, class_name)) != 0 ][0]
                for image in images:
                    #only download images that starts with http
                    src_link = image.get_attribute("src")
                    if(("http" in src_link) and (not "encrypted" in src_link)):
                        print(
                            f"[INFO] {self.search_key} \t #{count} \t {src_link}")
                        image_urls.append(src_link)
                        count +=1
                        break
            except Exception:
                print("[INFO] Unable to get link")

            try:
                #scroll page to load next image
                if(count%3==0):
                    self.driver.execute_script("window.scrollTo(0, "+str(indx_1*60)+");")
                element = self.driver.find_element(By.CLASS_NAME,"mye4qd")
                element.click()
                print("[INFO] Loading next page")
                time.sleep(3)
            except Exception:
                time.sleep(1)

        self.driver.quit()
        print("[INFO] Google search ended")
        return image_urls

    def save_images(self,image_urls, keep_filenames):
        """
            This function takes in an array of image urls and save it into the given image path/directory.
            Example:
                google_image_scraper = GoogleImageScraper("webdriver_path","image_path","search_key",number_of_photos)
                image_urls=["https://example_1.jpg","https://example_2.jpg"]
                google_image_scraper.save_images(image_urls)
        """
        print("[INFO] Saving images, please wait...")
        for indx,image_url in enumerate(image_urls):
            try:
                print("[INFO] Image url:%s"%(image_url))
                search_string = ''.join(e for e in self.search_key if e.isalnum())
                
                # Download image with timeout
                image = requests.get(image_url, timeout=10)
                if image.status_code == 200:
                    # Try to open the image
                    try:
                        image_from_web = Image.open(io.BytesIO(image.content))
                        
                        # Generate filename
                        if keep_filenames:
                            o = urlparse(image_url)
                            image_url = o.scheme + "://" + o.netloc + o.path
                            name = os.path.splitext(os.path.basename(image_url))[0]
                            filename = "%s.%s"%(name, image_from_web.format.lower() if image_from_web.format else 'jpg')
                        else:
                            # Use original format, fallback to jpg if format is unknown
                            ext = image_from_web.format.lower() if image_from_web.format else 'jpg'
                            filename = "%s%s.%s"%(search_string, str(indx), ext)

                        image_path = os.path.join(self.image_path, filename)
                        
                        # Convert to RGB if necessary
                        if image_from_web.mode in ('RGBA', 'LA', 'P'):
                            image_from_web = image_from_web.convert('RGB')
                        
                        # Save the image
                        image_from_web.save(image_path, quality=95)
                        print(f"[INFO] {self.search_key} \t {indx} \t Image saved at: {image_path}")
                        
                        # Check resolution only if both min and max are specified
                        if all(self.min_resolution) and all(self.max_resolution):
                            image_resolution = image_from_web.size
                            if (image_resolution[0] < self.min_resolution[0] or 
                                image_resolution[1] < self.min_resolution[1] or 
                                image_resolution[0] > self.max_resolution[0] or 
                                image_resolution[1] > self.max_resolution[1]):
                                print(f"[INFO] Image {filename} removed due to resolution constraints")
                                os.remove(image_path)
                        
                        image_from_web.close()
                        
                    except Exception as e:
                        print(f"[ERROR] Failed to process image: {str(e)}")
                        continue
                        
                else:
                    print(f"[ERROR] Failed to download image. Status code: {image.status_code}")
                    
            except Exception as e:
                print(f"[ERROR] Download failed: {str(e)}")
                continue
                
        print("--------------------------------------------------")
        print("[INFO] All downloads completed!")
