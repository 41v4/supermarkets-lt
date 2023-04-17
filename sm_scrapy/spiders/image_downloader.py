import datetime
import json
import os

import scrapy
from itemloaders.processors import MapCompose, TakeFirst
from loguru import logger
from scrapy.loader import ItemLoader

import helpers
from sm_scrapy.items import ImageItem
from sm_scrapy.settings import PARSED_DIR, SM_DIRS


class ImgDownloader(scrapy.Spider):
    name = "img_downloader"
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'CONCURRENT_REQUESTS_PER_IP': 1
    }

    def start_requests(self):
        DATE_ARG = getattr(self, 'date', None) # scrapy crawl img_downloader -a date=2023_04_16
        SM_ARG = getattr(self, 'sm', None) # scrapy crawl img_downloader -a sm=maxima

        # Date argument validation
        if DATE_ARG and not helpers.is_valid_date_arg(date_arg=DATE_ARG):
            logger.error(f"Invalid 'date' arg.: {DATE_ARG}")
            return False
        
        # Supermarket argument validation
        if SM_ARG:
            if not helpers.is_valid_sm_arg(sm_arg=SM_ARG):
                logger.error(f"Invalid 'sm' arg.: {SM_ARG}")
                return False
        else:
            logger.error(f"Missing 'sm' arg. Example usage: scrapy crawl img_downloader -a sm=maxima")
            return False
            
        DATE_DIR = DATE_ARG or datetime.date.today().strftime("%Y_%m_%d")
        base_dir = os.path.join(os.getcwd(), PARSED_DIR, SM_DIRS.get(SM_ARG.upper()), DATE_DIR)
            
        # Base dir. validation
        if not os.path.exists(base_dir):
            logger.error(f"Parsed dir. does not exist: {base_dir}")
            return False
        
        # read JSON files from local storage
        for fn in os.listdir(base_dir):
            if fn.endswith('.json'):
                fn_num = fn.split('.json')[0].strip()
                fp = os.path.join(base_dir, fn)
                with open(fp, 'r') as f:
                    json_data = json.load(f)
                img_url = json_data.get("img_url")
                # create a request object with the img URL
                request = scrapy.Request(img_url, self.parse, meta={"fn_num": fn_num})
                # yield the request object
                yield request

    def parse(self, response):
        item_loader = ItemLoader(item=ImageItem(), selector=response)

        fn_num = response.meta["fn_num"]
        item_loader.add_value("fn_num", fn_num)

        img_body = response.body
        item_loader.add_value("img_body", img_body)

        yield item_loader.load_item()