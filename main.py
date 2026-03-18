import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime

BASE_URL = "http://books.toscrape.com/"
OUTPUT_FILE = "output.csv"


def fetch_page(url: str) -> str:
    """
    Fetch the HTML content of a page and ensure proper UTF-8 encoding.

    Args:
        url (str): URL of the page to fetch.

    Returns:
        str: HTML content of the page.
    """
    response = requests.get(url)
    response.raise_for_status()
    response.encoding = "utf-8"  # Force UTF-8 to avoid encoding issues
    return response.text


def parse_books(html: str) -> list[dict]:
    """
    Parse the HTML page and extract book data (title, price, availability).

    Args:
        html (str): HTML content of the page.

    Returns:
        list[dict]: List of books with keys 'title', 'price', 'availability'.
    """
    soup = BeautifulSoup(html, "html.parser")
    books = []

    for article in soup.select("article.product_pod"):
        title = article.h3.a["title"].strip()
        price = article.select_one(".price_color").text.strip()
        availability = article.select_one(".availability").text.strip()

        books.append({"title": title, "price": price, "availability": availability})

    return books


def save_to_csv(data: list[dict], filename: str = OUTPUT_FILE) -> None:
    """
    Save scraped book data to a CSV file, adding a new column for today's date.
    Preserves historical data and adds new books automatically.

    Args:
        data (list[dict]): List of scraped book data.
        filename (str): Path to the CSV file.
    """
    today = datetime.now().strftime("%Y-%m-%d")
    new_column = f"price_{today}"

    file_exists = os.path.exists(filename)

    # If CSV does not exist, create it with today's prices
    if not file_exists:
        with open(filename, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=["title", new_column])
            writer.writeheader()
            for item in data:
                writer.writerow({"title": item["title"], new_column: item["price"]})
        return

    # If CSV exists, read existing data
    with open(filename, "r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        existing_rows = list(reader)
        fieldnames = reader.fieldnames or []

    # Add today's column if it does not exist
    if new_column not in fieldnames:
        fieldnames.append(new_column)

    # Map scraped data for quick access by title
    new_data = {item["title"]: item["price"] for item in data}

    existing_titles = set()
    for row in existing_rows:
        title = row["title"]
        existing_titles.add(title)
        row[new_column] = new_data.get(title, "")

    # Add new books that were not in CSV
    for title, price in new_data.items():
        if title not in existing_titles:
            new_row = {field: "" for field in fieldnames}
            new_row["title"] = title
            new_row[new_column] = price
            existing_rows.append(new_row)

    # Rewrite CSV with updated data
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing_rows)


if __name__ == "__main__":
    # Fetch HTML from the base URL
    html_content = fetch_page(BASE_URL)

    # Parse books data
    books_list = parse_books(html_content)

    # Save or update CSV with scraped data
    save_to_csv(books_list)
