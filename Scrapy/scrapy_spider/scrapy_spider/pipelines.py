# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ScrapySpiderPipeline:
    def open_spider(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
    
    def close_spider(self, spider):
        spider.logger.info("Spider closed: %s" % spider.name)
        
    def process_item(self, item, spider):
        return item
