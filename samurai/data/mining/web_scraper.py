from bs4 import BeautifulSoup
import httpx
from selenium.common.exceptions import NoSuchElementException

import time, random
import logging

import samurai.data.mining.pdf_scraper as pdf_scraper
from samurai.logger import setup_logger

from selenium.webdriver.common.by import By
from selenium import webdriver

def check_and_bypass_message(driver):
    logger = logging.getLogger(__name__)
    if(driver.find_elements(By.ID, 'sds-dialog-0')):
        logger.info("Message detected. Passing driver to bypasser")
        past_message(driver)

def past_message(driver):
    logger = logging.getLogger(__name__)
    driver.execute_script("document.getElementById('sds-dialog-0').scrollTop = 5000;")
    
    box = driver.find_element(By.CLASS_NAME, 'sds-dialog-actions')
    button = box.find_element(By.CLASS_NAME, 'usa-button')
    
    if button:
        logger.info("Found button. Clicking")
        button.click()
        
def setup_driver():
    logger = logging.getLogger(__name__)
    logger.info("Setting up headless Chrome driver")
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(3)
    
    return driver

def scrape_contract_page(url: str, driver=None, scrape_description=True,
                         scrape_attachments=True):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    
    logger.info(f"Scraping contract page {url}")
   
    if driver is None:
        driver = setup_driver()
       
    driver.get(url) 
    check_and_bypass_message(driver)
    
    logger.debug(driver.page_source)
    soup = BeautifulSoup(driver.page_source, "lxml")
    
    logger.debug(soup.text)
    
    if scrape_description: 
        logger.info(f"Scraping description for {url}")
        description_html = driver.find_element(By.ID, "description")
        if description_html is None:
            logger.warning(f"No description found for {url}")
            description = ""
        else:
            description = description_html.text
    else:
        description = "" 
        
    attachments = [] 
  
    if scrape_attachments:
        logger.info(f"Scraping attachments for {url}")
        try:
            attachment_element = driver.find_element(By.ID, "attachments-links")
        except NoSuchElementException:
            logger.warning("Attachment rows not found. Most likely 404")
            return {"description" : description, "attachments" : attachments} 
        driver.execute_script("arguments[0].scrollIntoView(true)", attachment_element)
        
        attachment_rows = driver.find_elements(By.CLASS_NAME, "upload-table-row")
        logger.info(f"Attachment rows: {[x.text for x in attachment_rows]}")
        
        for i, row in enumerate(attachment_rows):
            try:
                link = row.find_element(By.TAG_NAME, "a").get_attribute('href')
            except NoSuchElementException:
                logger.warning(f"Unable to load attachment for {row.text}. Skipping...")
                continue
                
            logger.info(f"Scraping attachment {i + 1} out of {len(attachment_rows)}")
            content = pdf_scraper.scrape_attachment(link)
            
            time.sleep(random.uniform(2, 4))
            
            attachments.append(content)
            logger.debug(f"Scraped from attachment: {content}")
        
        logger.info(f"Scraped {len(attachments)} attachments out of {len(attachment_rows)}")
  
    sleep = random.uniform(1, 2)
    logger.info(f"Sleeping for {sleep} seconds...")
    time.sleep(sleep)
    
    return {"description" : description, "attachments" : attachments} 
    
if __name__ == "__main__":
    setup_logger()
    print(scrape_contract_page("https://sam.gov/opp/075946bc04934e9d894b7983d50a710a/view"))