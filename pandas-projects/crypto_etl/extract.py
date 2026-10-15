import requests
from config import headers, params
import logging

logger = logging.getLogger(__name__)


def extract(url):

    logger.info("Starting Crypto API request")

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=30
        )

        logger.info(f"API status code: {response.status_code}")

        response.raise_for_status()

        data = response.json()

        logger.info("Extraction completed")

        return data

    except requests.RequestException:
        logger.exception("Crypto API request failed")
        return None

    except Exception:
        logger.exception("Unexpected error during extraction")
        return None