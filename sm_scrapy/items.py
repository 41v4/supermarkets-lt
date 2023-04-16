import scrapy
from itemloaders.processors import MapCompose, TakeFirst


class MaximaHtmlItem(scrapy.Item):
    page_num = scrapy.Field(output_processor=TakeFirst())
    html = scrapy.Field(output_processor=TakeFirst())
