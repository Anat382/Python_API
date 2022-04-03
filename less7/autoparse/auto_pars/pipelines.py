# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy


class AutoParsPipeline:
    def process_item(self, item, spider):
        print()
        return item

class AutoPhotosPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        print()
        # item['photos'] = list(filter(lambda x: x if not x.find('https') else '', item['photos']))
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    # def file_path(self, request, response=None, info=None, *, item=None):
    #     pass= [itm[1] for itm in results if itm[0]]
    #     return item