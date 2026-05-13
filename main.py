
import time
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

SEARCH_URL = "https://www.sahibinden.com/toyota-corolla"

seen = set()

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })

def parse_price(text):
    text = text.replace("TL", "").replace(".", "").replace(",", "").strip()
    digits = ''.join(filter(str.isdigit, text))
    return int(digits) if digits else 0

def scrape():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(SEARCH_URL, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")

    listings = soup.select(".searchResultsItem")

    for item in listings[:20]:
        try:
            title = item.select_one(".classifiedTitle").get_text(strip=True)
            price_text = item.select_one(".classified-price-container").get_text(strip=True)

            price = parse_price(price_text)

            if title in seen:
                continue

            seen.add(title)

            # Basit fırsat filtresi
            if price < 1400000:
                msg = f"FIRSAT ILAN\n\n{title}\nFiyat: {price:,} TL"
                print(msg)
                send_telegram(msg)

        except Exception as e:
            print("Hata:", e)

while True:
    scrape()
    time.sleep(120)
