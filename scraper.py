import requests
from bs4 import BeautifulSoup

URL = "https://fmhy.net/video"

def get_live_sports_urls():
    resp = requests.get(
        URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    header = soup.find("h3", id="live-sports")
    if not header:
        raise RuntimeError("live-sports header not found")

    ul = header.find_next_sibling("ul")
    if not ul:
        raise RuntimeError("live-sports <ul> not found")

    urls = []

    for li in ul.find_all("li", class_="starred", recursive=False):
        first_link = li.find("a", href=True)
        if first_link:
            urls.append(first_link["href"])

    return urls
