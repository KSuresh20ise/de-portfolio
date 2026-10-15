import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv(override=True)


# Database configuration
USER_NAME = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DATABASE = os.getenv("DB_NAME")

# API configuration
API_KEY = os.getenv("API_KEY")


# Validate environment variables
if not all([USER_NAME, DB_PASSWORD, DATABASE, API_KEY]):
    raise ValueError(
        "Missing required environment variables. "
        "Check your .env file."
    )


# Encode password for database connection URL
PASSWORD = quote_plus(DB_PASSWORD)


# CoinGecko API
BASE_URL = "https://api.coingecko.com/api/v3"
URL = f"{BASE_URL}/coins/markets"

headers = {
    "accept": "application/json",
    "x-cg-demo-api-key": API_KEY
}

params = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 250,
    "page": 1,
    "sparkline": False
}