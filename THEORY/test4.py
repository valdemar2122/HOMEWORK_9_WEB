import requests
from bs4 import BeautifulSoup

domain = "https://webscraper.io"
start_url = "/test-sites/e-commerce/static/"
response = requests.get(f"{domain}{start_url}")

soup = BeautifulSoup(response.text, "html.parser")
side_menu = soup.find("ul", id="side-menu")
links = side_menu.find_all("a")

links.pop(0)
links_to_scrape = []
for link in links:
    links_to_scrape.append(f'{domain}{link["href"]}')

for link in links_to_scrape:
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")

    captions = soup.find_all("div", class_="caption")

    for caption in captions:
        price = caption.find("h4", class_="price").text
        name = caption.find("a").text
        print(f"{name} with price {price}")
