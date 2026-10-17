import re
import requests
from bs4 import BeautifulSoup
from typing import Dict

try:
    from .utils import save_to_json
except ImportError:
    from utils import save_to_json


def fetch_wikipedia_page(url: str) -> str:
    """
    Fetch the HTML content of the given Wikipedia page.

    Args:
        url (str): The URL of the Wikipedia page to fetch.

    Returns:
        str: The HTML content of the page as a string.

    Raises:
        requests.HTTPError: If the HTTP request returned an unsuccessful status code.
        requests.RequestException: If there was a network error.
    """
    # Wikipedia rejects requests without a descriptive User-Agent
    headers = {"User-Agent": "MLDS-Practical-Labs/1.0 (educational web scraping exercise)"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.text


def extract_title(soup: BeautifulSoup) -> str:
    """
    Extract the title of the Wikipedia page.

    Args:
        soup (BeautifulSoup): A BeautifulSoup object representing the parsed HTML.

    Returns:
        str: The title of the page, or an empty string if it is not found.
    """
    heading = soup.find("h1", id="firstHeading")
    return heading.get_text(strip=True) if heading else ""


def extract_first_sentence(soup: BeautifulSoup) -> str:
    """
    Extract the first sentence of the first paragraph on the Wikipedia page.

    Args:
        soup (BeautifulSoup): A BeautifulSoup object representing the parsed HTML.

    Returns:
        str: The first sentence of the first paragraph, or an empty string if there is none.
    """
    for paragraph in soup.find_all("p"):
        # Drop footnote markers such as [1] and collapse whitespace
        text = re.sub(r"\[[^\]]*\]", "", paragraph.get_text())
        text = re.sub(r"\s+", " ", text).strip()
        if not text:
            # Wikipedia has empty <p> elements before the real first paragraph
            continue
        # A sentence ends at . ! or ? followed by whitespace and a capital letter/digit
        match = re.search(r"(?<=[.!?])\s+(?=[A-Z0-9])", text)
        return text[:match.start()] if match else text
    return ""


if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/Web_scraping"
    try:
        page_content = fetch_wikipedia_page(url)
        soup = BeautifulSoup(page_content, 'html.parser')

        # Extract the title of the page
        title = extract_title(soup)

        # Extract the first sentence of the first paragraph
        first_sentence = extract_first_sentence(soup)

        # Combine the extracted data
        extracted_data = {
            "title": title,
            "first_sentence": first_sentence
        }

        # Print the extracted data
        print("Extracted Data:", extracted_data)

        # Save the data to a JSON file
        save_to_json(extracted_data, 'extracted_wikipedia_data.json')

        print("Data successfully saved to extracted_wikipedia_data.json")
    except Exception as e:
        print(f"An error occurred: {e}")
