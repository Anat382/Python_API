from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from auto_pars import settings
from auto_pars.spiders.olx_pars import OlxParsSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(OlxParsSpider, search='bmw')

    process.start()
