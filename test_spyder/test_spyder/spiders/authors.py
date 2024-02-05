import scrapy
from test_spyder.test_spyder.items import ScrapyQuoteItem, ScrapyAuthorsItem
from scrapy.crawler import CrawlerProcess


class QuoteSpider(scrapy.Spider):
    name = "authors"
    custom_settings = {"FEED_FORMAT": "json", "FEED_URI": "quotes.json"}
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def compose_quote(self, raw_quote):
        quote = ScrapyQuoteItem()
        quote["tags"] = raw_quote.xpath('div[@class="tags"]/a/text()').getall()
        quote["author"] = raw_quote.xpath('span/small[@class="author"]/text()').get()
        quote["quote"] = raw_quote.xpath("span[@class='text']/text()").get()

        return quote

    def parse(self, response):

        quotes = response.xpath("/html//div[@class='quote']")

        for quote in quotes:
            yield self.compose_quote(quote)

        next_page = response.xpath("//li[@class='next']/a/@href").get()

        if next_page is not None:
            yield scrapy.Request(url=self.start_urls[0] + next_page)


class AuthorsSpider(scrapy.Spider):
    name = "quotes"
    custom_settings = {"FEED_FORMAT": "json", "FEED_URI": "authors.json"}
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        # Select quotes
        for quote in response.xpath('//div[@class="quote"]'):
            # Extract author URL
            author_url = quote.xpath(
                './/span/small[@class="author"]/following-sibling::a/@href'
            ).get()
            if author_url:
                yield response.follow(author_url, callback=self.parse_author)

        # Follow pagination link if it exists
        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_author(self, response):
        author = ScrapyAuthorsItem()
        author["fullname"] = response.xpath(
            '//h3[@class="author-title"]/text()'
        ).extract_first()
        author["born_date"] = response.xpath(
            '//span[@class="author-born-date"]/text()'
        ).extract_first()
        author["born_location"] = (
            response.xpath('//span[@class="author-born-location"]/text()').get().strip()
        )
        author["description"] = (
            response.xpath('//div[@class="author-description"]/text()').get().strip()
        )

        yield author


def main():
    process = CrawlerProcess()
    process.crawl(QuoteSpider)
    process.start()

    process = CrawlerProcess()
    process.crawl(AuthorsSpider)
    process.start()


if __name__ == "__main__":
    main()
