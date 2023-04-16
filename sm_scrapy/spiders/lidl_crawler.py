import scrapy
from scrapy.loader import ItemLoader

from sm_scrapy.items import LidlHtmlItem
from urllib.parse import urljoin


class LidlCrawler(scrapy.Spider):
    name = "lidl_crawler"
    allowed_domains = ["lidl.lt"]
    start_urls = ["https://www.lidl.lt/pasiulymai"]

    def parse(self, response):
        partial_urls = response.css("div.nuc-m-flex-container__container article a.ret-o-card__link.nuc-a-anchor::attr(href)").getall()
        for partial_url in partial_urls:
            url = urljoin(response.url, partial_url)
            yield scrapy.Request(url, callback=self.dump_product_html)

    def dump_product_html(self, response):
        item_loader = ItemLoader(item=LidlHtmlItem(), selector=response)
        html = response.text
        item_loader.add_value('html', html)
        yield item_loader.load_item()
        
