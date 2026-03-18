# Competitor Price Tracker

Small demo of a Python tool to automatically scrape product prices from websites and maintain historical records in CSV format. Ideal for small businesses, e-commerce managers, or freelancers who want to monitor competitor pricing and availability over time.


## Features

- Scrapes product titles, prices, and availability from a website.
- Maintains historical prices with a new column for each scraping date.
- Handles new products automatically.
- Exports data in CSV format, ready for analysis.
- Can be extended to filter products or generate alerts.

## Technologies

- Python 3.8+
- [requests](https://pypi.org/project/requests/) → fetch web pages
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) → parse HTML
- CSV module → store historical data
- datetime → track scraping dates

## Possible improvements
This being a demo, many features can be added or improved to suit client need, such as
- Targetting specific products of categories
- Scraping more complex websites
- Generating reports with visuals of price evolution
- Automatic comparison with prices of your own products
- ...
