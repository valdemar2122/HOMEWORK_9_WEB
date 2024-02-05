from scrapy.crawler import CrawlerProcess
from test_spyder.test_spyder.spiders import authors
from seed import main


def processing():
    # Запуск процесса парсинга
    process = CrawlerProcess()
    process.crawl(authors.AuthorsSpider)
    process.crawl(authors.QuoteSpider)
    process.start()


if __name__ == "__main__":
    processing()
    main()
