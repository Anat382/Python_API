import scrapy
from scrapy.http import HtmlResponse
from auto_pars.items import AutoScraperItem
from scrapy.loader import ItemLoader

class OlxParsSpider(scrapy.Spider):
    name = 'olx_pars'
    allowed_domains = ['olx.kz']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://www.olx.kz/transport/legkovye-avtomobili/q-{kwargs.get('search')}/"]

    def parse(self, response: HtmlResponse):
       links = response.xpath("//a[contains(@class, 'thumb vtop inlblk')]/@href").getall()
       for link in links:
           yield response.follow(link, callback=self.parse_ads)


    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=AutoScraperItem(), response=response)
        loader.add_value("url", response.url)
        loader.add_xpath("name", "//div/h1/text()")
        loader.add_xpath("price", "//h3[contains(@class,'css-okktvh-Text')]/text()")
        loader.add_xpath("photos", "//img/@src")
        loader.add_xpath("description", "//div[contains(@data-cy, 'ad_description')]//div/text()")
        yield loader.load_item()
