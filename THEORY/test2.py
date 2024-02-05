import requests
from bs4 import BeautifulSoup

url = "http://quotes.toscrape.com/"
page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")

first_paragraph = soup.find("p")
first_paragraph_text = first_paragraph.get_text()
print(first_paragraph_text.strip())


first_link = soup.find("a")
first_link_href = first_link["href"]
print(first_link_href)

body_children = list(first_paragraph.children)
print(body_children)


first_div = soup.find("div")
first_div_link = first_div.find("a")
print(first_div_link)

first_paragraph_parent = first_paragraph.parent
print(first_paragraph_parent)

container = soup.find("div", attrs={"class": "quote"}).find_parent(
    "div", class_="col-md-8"
)
print(container)
