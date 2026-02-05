import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import io


HEADERS = {"User-Agent" : "Mozilla/5.0"}

TARGET_KEYWORDS = [
    "knee replacement",
    "hip replacement",
    "ivf",
    "bariatric",
    "cataract",
    "lasik",
    "liposuction",
    "breast",
    "c-section",
    "cesarean"
]

# Find price transparency file link
# ------------------------------------------------


def find_price_file(hospital_url):

    try:
        r = requests.get(hospital_url, headers = HEADERS, timeout = 25)
        soup = BeautifulSoup(r.text, "html.parser")

        links = soup.find_all("a", href = True)
        keywords = [
            "price", "transparency", "standard",
            "chargemaster", "machine", "mrf"
        ]

        for link in links:
            href = link["href"]

            if any(k in href.lower() for k in keywords):
                if href.startwith("/"):
                    href = hospital_url.rstrip("/") + href
                return href
        return None

    except Exception as e:
        return str(e)


# Stream JSON and filter relevant procedures
# -------------------------------------------------


def extract_relevant_from_json_stream(file_url, max_rows = 2000):

    try:
        r = requests.get(file_url, headers = HEADERS, stream = True, timeout =60)
        content = r.content[:5_000_000]   # only first ~5MB for MVP test
        data = json.load(content)

        results = []

        def search_obj(obj):
            if len(results) >= max_rows:
                return

            if isinstance(obj, dict):
                text = str(obj).lower()
                if any(k in text for k in TARGET_KEYWORDS):
                    results.append(obj)
                for  v in obj.values():
                    search_obj(v)

            
            elif isinstance(obj, list):
                for item in obj:
                    search_obj(item)
        
        search_obj(data)

        return pd.DataFrame(results)
        
    except Exception as e:
        return pd.DataFrame({"error": [str(e)]})



# Main wrapper function
# -------------------------------------------------


def run_scraper(hospital_name, hospital_url):

    file_link = find_price_file(hospital_url)

    if not file_link:
        return None, "No transparency file found"

    df = extract_relevant_from_json_stream(file_link)

    if isinstance(df, pd.DataFrame):
        df["hospital"] = hospital_name

    return df, file_link



