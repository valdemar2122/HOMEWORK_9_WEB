import requests
from bs4 import BeautifulSoup

url = "https://www.bbc.com/ukrainian"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
html = soup.prettify()

headers = soup.find_all("div", class_="promo-text")

for header in headers:
    print(header.find("a").text)

    time = header.find("time")

    if time is not None:
        print(time.text)
