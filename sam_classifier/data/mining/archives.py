import pandas as pd
import codecs
from io import StringIO
import os
import datetime
import logging

import sam_classifier.data.mining.web_scraper as web_scraper
from sam_classifier.logger import setup_logger
import sam_classifier.data.mining.utils as utils

def filter_raw_archives():
    with codecs.open("/Users/thaivillaluna/Downloads/sam_archive.csv", 'r', encoding='utf-8',
                 errors='ignore') as fdata:
        df = pd.read_csv(StringIO(fdata.read()), low_memory=False, index_col=0)
    df = df[df["NaicsCode"] == "541330"]
    
    df.to_csv("../../files/archives/1_filtered_raw_archives.csv")
    
def scrape_archive_urls():
    logger = logging.getLogger(__name__)
    DIR = "../../files/archives/split_by_date/"
    
    for file in os.listdir(DIR):
        if not file.endswith(".csv"):
            logger.info(f"Skipping {file} because not csv format")
            continue 
      
        if file in os.listdir(DIR + "/attachments_scraped/"):
            logger.info(f"Skipping {file} because previously scraped")
            continue
        
        logger.info(f"Creating dataframe from file: {file}")
        df = pd.read_csv(DIR + file, index_col=0)
   
        driver = web_scraper.setup_driver()
    
        logger.info(f"Applying scrape_contract_page() to dataframe") 
        results = df['Link'].apply(web_scraper.scrape_contract_page, 
                                        driver=driver, scrape_description=False,
                                        scrape_attachments=True)
        
        attachments = [result.get("attachments") for result in results]
        attachments = [' '.join(filter(None, row)) for row in attachments]
        df['Attachments'] = attachments
      
        logger.info(f"Writing dataframe to file: {file}") 
        df.to_csv(DIR + "/attachments_scraped/" + file) 
       

def split_into_dates():
    df = pd.read_csv("../../files/archives/1_filtered_raw_archives.csv", index_col=0)
    print(df.head())
    dates = utils.get_dates()
    
    for date in dates:
        dt = datetime.datetime.strptime(date, "%m-%d-%Y")
        date_str = dt.strftime("%Y-%m-%d")
        date_filtered_df = df[df["PostedDate"].str.contains(date_str)]
        
        date_filtered_df.to_csv(f"../../files/archives/split_by_date/{dt.strftime("%m-%d-%Y")}.csv")

def main():
    setup_logger()
    split_into_dates()
    scrape_archive_urls()

if __name__=="__main__":
    main()