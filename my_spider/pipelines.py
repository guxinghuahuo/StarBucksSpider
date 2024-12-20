# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from my_spider.spiders.starbucks import StarbucksSpider
import csv

class MySpiderPipeline:
    def __init__(self):
        # 打开 CSV 文件，准备写入
        self.file = open('starbucks.csv', 'w', encoding='utf-8', newline='')
        self.writer = csv.writer(self.file)
        # 如果文件为空，则写入表头
        self.writer.writerow(['Name', 'URL'])

    def process_item(self, item, spider):
        # 提取菜品名称和图片路径
        name = item.get("name")
        path = item.get("path")
        if name and path:
            # 构建完整的 URL
            url = StarbucksSpider.start_urls[0][:-6] + path
            # 写入 CSV 文件
            self.writer.writerow([name, url])
        return item

    def close_spider(self, spider):
        # 关闭 CSV 文件
        self.file.close()

        