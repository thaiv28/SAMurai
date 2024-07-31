import logging
from pathlib import Path
from collections import defaultdict
import datetime, time, random
import os
import httpx

import pandas as pd
from bs4 import BeautifulSoup

import sam_classifier.data.mining.utils as utils
from sam_classifier.logger import setup_logger

START_DATE = ""
END_DATE = ""

def init_search_terms(limit=100, posted_from=None,
                      posted_to=None, ptype=None, ncode=None):
    api_key = os.getenv('SAM_API_KEY')
    print(api_key)
    if not api_key:
        print("Valid API Key not found")
        exit(-1)
    
    if not posted_to:
        posted_to = datetime.date.today().strftime("%m/%d/%Y") 
        
    if not posted_from:
        posted_from = posted_to

    terms = {}
    terms['limit'] = limit
    terms['postedFrom'] = posted_from
    terms['postedTo'] = posted_to
    terms['api_key'] = api_key
    terms['ncode'] = ncode
    terms['pcode'] = ptype
    
    
    return terms


def send_sam_request(terms):
    search = f"https://api.sam.gov/prod/opportunities/v2/search?api_key={terms.get('api_key')}"

    for key, value in terms.items():
        if(key == 'api_key'):
            continue
        if not terms.get(key):
            continue
        
        if isinstance(terms.get(key), list):
            for search_term in value:
                search += f"&{key}={search_term}"
        else:
            search += f"&{key}={value}"
    
    return search

def get_dates():
    f = open("../files/dates.txt", "r")
    
    dates = f.readlines()
    dates = [date.strip() for date in dates]
    return dates

def main():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    
    contracts = []
  
    dates = get_dates()
    logger.debug(dates)
    
    for date in dates:
        terms = init_search_terms(ncode=541330, ptype=['r', 'o', 's', 'k'], posted_from=date,
                                posted_to=date)
        search = send_sam_request(terms)
    
        logger.debug(search)
        
        response = httpx.get(search)
        results_json = response.json()
        
        if response.status_code != httpx.codes.OK:
            logger.critical(results_json.get('error').get('message'))
            exit(1)
    
        logger.debug(results_json) 
        # sets contracts to a list of dictionaries, one for each contract
        contracts += results_json['opportunitiesData']
    
        logger.debug("\n".join([d.get("title") for d in contracts[-10:]]))
        
        time.sleep(random.randint(0, 2))
       
        df = pd.DataFrame.from_records(contracts) 
        df.to_csv(f"../files/temp/{date}.csv")
  
    # preprocess data
    logger.info(df) 
    
    return df
    
if __name__=="__main__":
    setup_logger()
    main()