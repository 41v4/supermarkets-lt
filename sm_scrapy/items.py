import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def clean_str(value):
    replaceable = [
        ('\n', ''),
        ('\xa0', ' '),
    ]
    for i in replaceable:
        from_str = i[0]
        to_str = i[-1]
        value = value.replace(from_str, to_str)
    value = " ".join(value.split())
    return value.strip()

def clean_discount(value):
    return value.replace("%", "").strip()

def clean_price(value):
    replaceable = [
        ('€', ''),
        (',', '.'),
    ]
    for i in replaceable:
        from_str = i[0]
        to_str = i[-1]
        value = value.replace(from_str, to_str)
    value = " ".join(value.split())
    return value.strip()


class MaximaHtmlItem(scrapy.Item):
    page_num = scrapy.Field(output_processor=TakeFirst())
    html = scrapy.Field(output_processor=TakeFirst())

class MaximaProductItem(scrapy.Item):
    name = scrapy.Field(input_processor=MapCompose(clean_str), output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(clean_str, clean_price), output_processor=TakeFirst())
    discount = scrapy.Field(input_processor=MapCompose(clean_str, clean_discount), output_processor=TakeFirst())
    product_url = scrapy.Field(output_processor=TakeFirst())
    img_url = scrapy.Field(output_processor=TakeFirst())
    descr = scrapy.Field(output_processor=TakeFirst())
    card_required = scrapy.Field(output_processor=TakeFirst())
    app_required = scrapy.Field(output_processor=TakeFirst())
    valid_from = scrapy.Field(input_processor=MapCompose(clean_str), output_processor=TakeFirst())
    valid_to = scrapy.Field(input_processor=MapCompose(clean_str), output_processor=TakeFirst())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_all_as_none()

    def set_all_as_none(self):
        for key, _ in self.fields.items():
            self[key] = None

class LidlHtmlItem(scrapy.Item):
    page_num = scrapy.Field(output_processor=TakeFirst())
    html = scrapy.Field(output_processor=TakeFirst())

class LidlProductItem(scrapy.Item):
    fn_num = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(input_processor=MapCompose(clean_str), output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(clean_str, clean_price), output_processor=TakeFirst())
    discount = scrapy.Field(input_processor=MapCompose(clean_str, clean_discount), output_processor=TakeFirst())
    unit_pricing = scrapy.Field(input_processor=MapCompose(clean_str), output_processor=TakeFirst())
    weight = scrapy.Field(input_processor=MapCompose(clean_str), output_processor=TakeFirst())
    product_url = scrapy.Field(output_processor=TakeFirst())
    img_url = scrapy.Field(output_processor=TakeFirst())
    descr = scrapy.Field(input_processor=MapCompose(clean_str)) # multiple values
    card_required = scrapy.Field(output_processor=TakeFirst())
    app_required = scrapy.Field(output_processor=TakeFirst())
    valid_from = scrapy.Field(output_processor=TakeFirst()) # str 'YYYY-MM-DD'
    valid_to = scrapy.Field(output_processor=TakeFirst()) # str 'YYYY-MM-DD'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_all_as_none()

    def set_all_as_none(self):
        for key, _ in self.fields.items():
            self[key] = None