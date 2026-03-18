import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime



BASE_URL = "http://books.toscrape.com/"


def fetch_page(url):
    response = requests.get(url)
    response.raise_for_status()
    response.encoding = "utf-8"
    return response.text


def parse_books(html):
    soup = BeautifulSoup(html, "html.parser")
    books = []

    for article in soup.select("article.product_pod"):
        title = article.h3.a["title"]
        price = article.select_one(".price_color").text
        availability = article.select_one(".availability").text.strip()

        books.append({
            "title": title,
            "price": price,
            "availability": availability
        })

    return books


def save_to_csv(data, filename="output.csv"):
    today = datetime.now().strftime("%Y-%m-%d")
    new_column = f"price_{today}"

    file_exists = os.path.exists(filename)

    # Si le fichier n'existe pas → création normale
    if not file_exists:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["title", new_column])
            writer.writeheader()
            for item in data:
                writer.writerow({
                    "title": item["title"],
                    new_column: item["price"]
                })
        return

    # Sinon → lecture du fichier existant
    with open(filename, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        existing_rows = list(reader)
        fieldnames = reader.fieldnames

    # Ajouter la nouvelle colonne si elle n'existe pas
    if new_column not in fieldnames:
        fieldnames.append(new_column)

    # Convertir les données scrapées en dict {title: price}
    new_data = {item["title"]: item["price"] for item in data}

    # Mettre à jour les lignes existantes
    existing_titles = set()
    for row in existing_rows:
        title = row["title"]
        existing_titles.add(title)
        row[new_column] = new_data.get(title, "")

    # Ajouter les nouveaux livres qui n'existaient pas
    for title, price in new_data.items():
        if title not in existing_titles:
            new_row = {field: "" for field in fieldnames}
            new_row["title"] = title
            new_row[new_column] = price
            existing_rows.append(new_row)

    # Réécrire le fichier avec la nouvelle colonne
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing_rows)


if __name__ == "__main__":
    html = fetch_page(BASE_URL)
    books = parse_books(html)
    save_to_csv(books)