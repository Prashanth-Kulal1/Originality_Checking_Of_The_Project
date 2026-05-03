import requests
from bs4 import BeautifulSoup

def get_text(url):
    try:
        res = requests.get(url, timeout=5, headers={
            "User-Agent": "Mozilla/5.0"
        })

        soup = BeautifulSoup(res.text, "html.parser")

        # remove junk
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        text = soup.get_text(separator=" ")

        # clean extra spaces
        text = " ".join(text.split())

        return text

    except:
        return None