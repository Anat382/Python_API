from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from jobparser import settings

# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.log import configure_logging
# from twisted.internet import reactor
# from scrapy.utils.project import get_project_settings

from jobparser.spiders.hhru import HhruSpider
from jobparser.spiders.superjob import SuperjobSpider

if __name__ == '__main__':

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    crawler_process = CrawlerProcess(settings=crawler_settings)
    crawler_process.crawl(HhruSpider)
    # crawler_process.crawl(SuperjobSpider)
    crawler_process.start()


    # запуск пауков происходит поочередно, не паралельно !!!!!!!!!, в данном пожходе не отрабатывает дебаг
    # configure_logging()
    # settings_ = get_project_settings()
    # runner = CrawlerRunner(settings_)
    # runner.crawl(HhruSpider)
    # runner.crawl(SuperjobSpider)
    # concat_run = runner.join()
    # concat_run.addBoth(lambda  _: reactor.stop())
    #
    # reactor.run()