import salary as salary
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SuperjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    base_url = 'https://spb.superjob.ru'
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bt%5D%5B0%5D=4', 'https://spb.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response: HtmlResponse):
        next_page = SuperjobSpider.base_url + response.xpath("//a[@rel='next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@target='_blank']/@href").getall()
        print(links)
        for link in links:
            yield response.follow(SuperjobSpider.base_url + link, callback=self.vacancy_parse)


    def vacancy_parse(self, response: HtmlResponse):
        name_value = response.css('h1::text').get()
        salary_value = response.xpath("//span[contains(@class,'_2Wp8I _1BiPY _26ig7 _18w_0')]/text()").getall()
        url_value = response.url
        yield JobparserItem(name=name_value, salary=salary_value, url=url_value)
