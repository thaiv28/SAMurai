from tika import parser
import httpx

import logging

def scrape_attachment(download_url: str):
    logger = logging.getLogger(__name__)
   
    response = httpx.get(download_url, follow_redirects=True)
    text = parser.from_buffer(response.content)["content"]
    
    return text
    
if __name__=="__main__":
    pass