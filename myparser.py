import requests
from bs4 import BeautifulSoup
import json


# function to get info from page
def scrape_quotes(url):
    quotes = []
    # get the content of page
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    for quote in soup.find_all("div", class_="quote"):
        text = quote.find("span", class_="text").text
        author = quote.find("small", class_="author").text
        tags = [tag.text for tag in quote.find_all("a", class_="tag")]

        quotes.append({"tags": tags, "author": author, "quote": text})
    return quotes


# Function to scrape information about authors from their "about" page
def scrape_author_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extracting author information
    fullname = soup.find("h3", class_="author-title").text.strip()
    born_date = soup.find("span", class_="author-born-date").text.strip()
    born_location = soup.find("span", class_="author-born-location").text.strip()
    description = soup.find("div", class_="author-description").text.strip()

    author_info = {
        "fullname": fullname,
        "born_date": born_date,
        "born_location": born_location,
        "description": description,
    }
    return author_info


# Function to scrape "about" links from a single page
def scrape_about_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    about_links = soup.find_all("a", href=True)
    return [link["href"] for link in about_links if link["href"].startswith("/author/")]


def main():
    # getting quotes
    base_url = "https://quotes.toscrape.com"
    all_quotes = []
    # scraping first page
    quotes = scrape_quotes(base_url)
    all_quotes.extend(quotes)

    # iterate to next pages if they are exist
    page = 2
    num_pages = 10  # Update this with the actual number of pages

    while True:
        url = f"{base_url}/page/{page}/"
        quotes = scrape_quotes(url)
        if not quotes:
            break
        all_quotes.extend(quotes)
        page += 1

    # getting authors
    all_about_links = set()

    # Loop through each page and scrape "about" links
    for page_num in range(1, num_pages + 1):
        page_url = base_url + "/page/" + str(page_num)
        about_links_on_page = scrape_about_links(page_url)
        all_about_links.update(about_links_on_page)

    authors_info = []

    # Loop through each "about" link, scrape author information, and store it
    for link in all_about_links:
        author_url = f"http://quotes.toscrape.com{link}"
        author_info = scrape_author_info(author_url)
        authors_info.append(author_info)

    # # save information to quotes.json file
    with open("quotes.json", "w") as f:
        json.dump(all_quotes, f, indent=4, ensure_ascii=False)

    # Saving authors' information to authors.json file
    with open("authors.json", "w") as f:
        json.dump(authors_info, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
