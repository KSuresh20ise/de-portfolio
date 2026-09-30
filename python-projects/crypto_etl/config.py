import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

USER_NAME = os.getenv("DB_USER")
PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))
DATABASE = os.getenv("DB_NAME")

API_KEY = os.getenv("API_KEY")

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