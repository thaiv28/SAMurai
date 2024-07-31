import httpx
import requests
import logging

import pandas as pd

logger = logging.getLogger(__name__)

def send_request(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    try:
        request = httpx.get(url, headers=headers)  
    except httpx.ReadTimeout:
        logger.critical(f"Read timeout for {url}")
        logger.critical(f"Exiting with error")
        exit()
        
    return request

def write_df_to_csv(df: pd.DataFrame): 
    logger.debug(f"Starting write csv to disk")
    df.index.name = "index" 
    # df = df.assign(is_model_card_scraped=False)
    df.to_csv("./hf_model_repos.csv")

if __name__ == "__main__":
    print(send_request("https://scrapfly.io/blog/how-to-scrape-without-getting-blocked-tutorial/").text)