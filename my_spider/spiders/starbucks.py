import scrapy
import re

from my_spider.items import MySpiderItem

class StarbucksSpider(scrapy.Spider):
    name = "starbucks"
    allowed_domains = ["starbucks.com.cn"]
    start_urls = ["https://www.starbucks.com.cn/menu/"]

    def parse(self, response):
        item = MySpiderItem()
        comments = response.xpath('//comment()').getall()
        # 遍历所有注释内容
        for comment in comments:
            # 处理每个注释内容
            # 去除注释标记
            clean_comment = re.sub(r'<!--(.*?)-->', r'\1', comment, flags=re.DOTALL)
            # 用 Scrapy 提供的 Selector 类解析注释内容
            # 注意：comment 是一个字符串，不是 Selector 对象
            sel = scrapy.Selector(text=clean_comment)

            # 提取 <li> 标签内容，包含 <div> 和 <strong> 标签
            for li in sel.xpath('//li'):
                # 提取 style 属性中的图片 URL
                style = li.xpath('.//div[@class="preview circle"]/@style').get()
                if style:
                    # 使用正则表达式提取 URL 中的图片地址
                    match = re.search(r'url\(["\']?([^"\')]+)["\']?\)', style)
                    if match:
                        item['path'] = match.group(1) # 获取图片 URL
                        # 提取 <strong> 标签中的菜品名称
                        item['name'] = li.xpath('.//strong/text()').get()

                        yield item
