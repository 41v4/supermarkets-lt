import datetime
import os

from itemadapter import ItemAdapter

from sm_scrapy.settings import HTML_DIR, SM_DIRS
from sm_scrapy.items import MaximaHtmlItem


class SmScrapyPipeline:
    CURRENT_DATE_DIR = datetime.date.today().strftime("%Y_%m_%d")
    def __init__(self):
        if not os.path.exists(HTML_DIR):
            os.mkdir(HTML_DIR)
        for sm_dir in SM_DIRS.values():
            joined_dir = os.path.join(HTML_DIR, sm_dir)
            if not os.path.exists(joined_dir):
                os.mkdir(joined_dir)

    def process_item(self, item, spider):
        if isinstance(item, MaximaHtmlItem):
            html_dir = os.path.join(HTML_DIR, SM_DIRS["MAXIMA"], self.CURRENT_DATE_DIR)
            if not os.path.exists(html_dir):
                os.mkdir(html_dir)
            self.store_html_maxima(item, html_dir)

    def store_html_maxima(self, item, html_dir):
        page_num = item["page_num"]
        html = item["html"]
        html_fp = os.path.join(html_dir, page_num + ".txt")
        with open(html_fp, 'w', encoding='utf-8') as f:
            f.write(html)
