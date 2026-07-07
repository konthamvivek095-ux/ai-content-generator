import requests
from bs4 import BeautifulSoup

def extract_content(url):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.text if soup.title else "No Title"

    paragraphs = soup.find_all("p")

    content = " ".join([p.get_text() for p in paragraphs])

    return {
        "title": title,
        "content": content
    }