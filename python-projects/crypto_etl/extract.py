import requests
from config import headers,params
from logger import logger
import logging

logger = logging.getLogger(__name__)

def extract(url):

    logger.info("Starting Crypto API request")
    try:
        response = requests.get(
            url,
            headers=headers,
            params=params
       )
        
          # Check the actual response from CoinGecko
        logger.info(f"API status code: {response.status_code}")

        if response.status_code != 200:
            logger.error(f"API response: {response.text}")

        

        data = response.json()

        logger.info("Extraction Completed")

        return data
    
    except requests.RequestException:
        logger.exception("Crypto API request failed")
        return None
    except Exception:
        logger.exception("Unexpected error during extraction")
        return None