import datetime
import os

import scrapy
from loguru import logger
from scrapy.loader import ItemLoader

import helpers
from sm_scrapy.items import LidlProductItem
from sm_scrapy.settings import HTML_DIR
from itemloaders.processors import MapCompose, TakeFirst


class LidlParser(scrapy.Spider):
    name = "lidl_parser"
    allowed_domains = ["lidl.lt"]
    start_urls = ["https://www.lidl.lt/pasiulymai"]

    def start_requests(self):
        DATE_ARG = getattr(self, 'date', None) # scrapy crawl maxima_parser -a date=2023_04_16

        # Date argument validation
        if DATE_ARG and not helpers.is_valid_date_arg(date_arg=DATE_ARG):
            logger.error(f"Invalid 'date' arg.: {DATE_ARG}")
            return False
            
        DATE_DIR = DATE_ARG or datetime.date.today().strftime("%Y_%m_%d")
        base_dir = os.path.join(os.getcwd(), HTML_DIR, "lidl", DATE_DIR)
            
        # Base dir. validation
        if not helpers.is_html_dir_exist(base_dir):
            logger.error(f"HTML dir. does not exist: {base_dir}")
            return False
        
        # read HTML files from local storage
        for fn in os.listdir(base_dir):
            if fn.endswith('.html'):
                fn_num = fn.split('.html')[0].strip()
                fp = os.path.join(base_dir, fn)
                with open(fp, 'r', encoding='utf-8') as f:
                    html = f.read()
                url = f'file://{fp}'
                # create a request object with the local file URL
                request = scrapy.Request(url, self.parse, meta={"fn_num": fn_num})
                # add the raw HTML as a meta field of the request
                request.meta['html'] = html
                # yield the request object
                yield request
    
    def parse(self, response):
        fn_num = response.meta["fn_num"]
        product_elem = response.css("article#productbox")

        item_loader = ItemLoader(item=LidlProductItem(), selector=product_elem)

        # fn_num
        item_loader.add_value('fn_num', fn_num)

        # name
        name = self.parse_name(product_elem)
        item_loader.add_value('name', name)

        # price
        price = self.parse_price(product_elem)
        item_loader.add_value('price', price)

        # discount
        discount = self.parse_discount(product_elem)
        item_loader.add_value('discount', discount)

        # unit_pricing
        unit_pricing = self.parse_unit_pricing(product_elem)
        item_loader.add_value('unit_pricing', unit_pricing)

        # weight
        weight = self.parse_weight(product_elem)
        item_loader.add_value('weight', weight)

        # product URL
        product_url = self.parse_product_url(response)
        item_loader.add_value('product_url', product_url)

        # product img
        img_url = self.parse_img(product_elem)
        item_loader.add_value('img_url', img_url)

        # descr
        descr = self.parse_desc(product_elem)
        item_loader.add_value('descr', descr)

        # card_required
        card_required = self.check_card_required(product_elem)
        item_loader.add_value('card_required', card_required)

        # app_required
        app_required = self.check_app_required(product_elem)
        item_loader.add_value('app_required', app_required)

        # valid_from
        valid_from = self.parse_valid_from(product_elem)
        item_loader.add_value('valid_from', valid_from)

        # valid_to
        valid_to = self.parse_valid_to(product_elem)
        item_loader.add_value('valid_to', valid_to)

        yield item_loader.load_item()

    def parse_name(self, elem):
        return elem.css("h1::text").get()

    def parse_price(self, elem):
        return elem.css("span.pricebox__price::text").get()

    def parse_discount(self, elem):
        discount = elem.css("div.pricebox__wrapper div.pricebox__highlight::text").get()
        if discount:
            is_discount_valid = helpers.is_discount_valid(value=discount)
            if is_discount_valid:
                return discount
            else:
                logger.error(f"Invalid discount: {discount.strip()}")
        return None
    
    def parse_unit_pricing(self, elem):
        return elem.css("div.pricebox__basic-quantity::text").get()
    
    def parse_weight(self, elem):
        weight = elem.css("span.pricebox__discount::text").get()
        if weight:
            is_weight_str_valid = helpers.is_weight_str_valid(weight)
            if is_weight_str_valid:
                return weight
            else:
                logger.error(f"Invalid weight: {weight.strip()}")
        return None
    
    def parse_product_url(self, elem):
        return elem.css('link[rel="canonical"]::attr(href)').get()
    
    def parse_img(self, elem):
        return elem.css("picture.picture--preview source::attr(data-srcset)").get()
    
    def parse_desc(self, elem):
        desc_lines = []
        li_elems =  elem.css("div.attributebox__long-description article.textbody li")
        for elem in li_elems:
            line = " ".join(elem.css("*::text").getall())
            desc_lines.append(line)
        return desc_lines
    
    def check_card_required(self, elem):
        return False
    
    def check_app_required(self, elem):
        app_required_elem = elem.xpath(
            "descendant-or-self::div[contains(translate(@data-list, 'ABCČDEFGHIJKLMNOPQRSTUŪVWXYZ', 'abcčdefghijklmnopqrstuūvwxyz'), 'lidl plus')]"
        ).get()
        return app_required_elem is not None
    
    def parse_valid_from(self, elem):
        date_str = elem.css("div.ribbon__text::text").get()
        dates = helpers.extract_lidl_dates(date_str)
        return dates.get("start_date")
    
    def parse_valid_to(self, elem):
        date_str = elem.css("div.ribbon__text::text").get()
        dates = helpers.extract_lidl_dates(date_str)
        return dates.get("end_date")
