from tika import parser
import httpx

import logging

def scrape_attachment(download_url: str):
    logger = logging.getLogger(__name__)
   
    response = httpx.get(download_url, follow_redirects=True)
    text = parser.from_buffer(response.content)["content"]
    
    return text
    
if __name__=="__main__":
    print(scrape_attachment("https://sam.gov/api/prod/opps/v3/opportunities/resources/files/710cce66de59485396d1cc5e82dea2fc/download?&token=be8bdaa9-71a5-49f2-951f-a6cc749d3104"))