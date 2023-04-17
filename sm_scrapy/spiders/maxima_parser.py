import datetime
import os

import scrapy
from loguru import logger
from scrapy.loader import ItemLoader

import helpers
from sm_scrapy.items import MaximaProductItem
from sm_scrapy.settings import HTML_DIR
from itemloaders.processors import MapCompose, TakeFirst


class MaximaParser(scrapy.Spider):
    name = "maxima_parser"
    allowed_domains = ["maxima.lt"]
    start_urls = ["https://www.maxima.lt/akcijos"]

    def start_requests(self):
        DATE_ARG = getattr(self, 'date', None) # scrapy crawl maxima_parser -a date=2023_04_16

        # Date argument validation
        if DATE_ARG and not helpers.is_valid_date_arg(date_arg=DATE_ARG):
            logger.error(f"Invalid 'date' arg.: {DATE_ARG}")
            return False
            
        DATE_DIR = DATE_ARG or datetime.date.today().strftime("%Y_%m_%d")
        base_dir = os.path.join(os.getcwd(), HTML_DIR, "maxima", DATE_DIR)
            
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
        product_elem = response

        item_loader = ItemLoader(item=MaximaProductItem(), selector=product_elem)

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
        item_loader.add_value('product_url', None)

        # product img
        img_url = self.parse_img(product_elem)
        item_loader.add_value('img_url', img_url)

        # descr
        descr = self.parse_descr(product_elem)
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
        return elem.css("h2.offer-modal-title::text").get()

    def parse_price(self, elem):
        price = ""
        price_eur = elem.css("div.price-eur::text").get()
        price_cents = elem.css("div span.price-cents::text").get()
        if price_eur:
            price += price_eur
            if price_cents:
                price += "." + price_cents
                is_price_valid = helpers.is_price_valid(value=price)
                if is_price_valid:
                    return price
                else:
                    logger.error(f"Invalid price: {price}")
        return None

    def parse_discount(self, elem):
        discount = elem.css("div.discount-icon h3::text").get()
        if discount:
            is_discount_valid = helpers.is_discount_valid(value=discount)
            if is_discount_valid:
                return discount
            else:
                logger.error(f"Invalid discount: {discount}")
        return None
    
    def parse_unit_pricing(self, elem):
        possible_lines = elem.css("div.offer-modal-card.h-100 div.text-small.mb-4::text").getall()
        for line in possible_lines:
            if helpers.is_unit_pricing_valid_maxima(line):
                return line
        return None
    
    def parse_weight(self, elem): # not exist
        return None
    
    def parse_img(self, elem):
        return elem.css("div.image-col-wrapper img.img-fluid::attr(src)").get()
    
    def parse_descr(self, elem):
        return elem.css("div.text-small.mb-3::text").get()
    
    def check_card_required(self, elem):
        card_required_elem = elem.xpath(
            "descendant-or-self::img[contains(translate(@alt, 'ABCČDEFGHIJKLMNOPQRSTUŪVWXYZ', 'abcčdefghijklmnopqrstuūvwxyz'), 'ačiū')]"
        ).get()
        return card_required_elem is not None
    
    def check_app_required(self, elem):
        app_required_elem = elem.xpath(
            "descendant-or-self::img[contains(translate(@alt, 'ABCČDEFGHIJKLMNOPQRSTUŪVWXYZ', 'abcčdefghijklmnopqrstuūvwxyz'), 'su program')]"
        ).get()
        return app_required_elem is not None
    
    def parse_valid_from(self, elem):
        date_str = elem.css("div.offer-modal-date::text").get()
        dates = helpers.extract_maxima_dates(date_str)
        return dates.get("start_date")
    
    def parse_valid_to(self, elem):
        date_str = elem.css("div.offer-modal-date::text").get()
        dates = helpers.extract_maxima_dates(date_str)
        return dates.get("end_date")
