import requests
from bs4 import BeautifulSoup
from app.repositories.extraction_repository import ExtractionRepository


class ExtractionService:

    def __init__(self):
        self.repo = ExtractionRepository()

    def extract_text(self, user_id, url):
        try:
            response = requests.get(url, timeout=10, verify=False)

            if response.status_code != 200:
                raise ValueError(f"Failed to fetch website: HTTP {response.status_code}")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to fetch URL: {str(e)}")
        
        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        title = soup.title.string.strip() if soup.title else "No Title"

        text = soup.get_text(separator="", strip=True)

        word_count = len(text.split())

        self.repo.save(user_id, url, title, word_count, text)

        return {
            "title": title,
            "word_count": word_count,
            "text" : text[:2000]
        }