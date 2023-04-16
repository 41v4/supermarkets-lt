import datetime
import json
import os
from pathlib import Path

from itemadapter import ItemAdapter

from sm_scrapy.items import MaximaHtmlItem, MaximaProductItem
from sm_scrapy.settings import HTML_DIR, PARSED_DIR, SM_DIRS


class SmScrapyPipeline:
    CURRENT_DATE_DIR = datetime.date.today().strftime("%Y_%m_%d")
    maxima_seq = 0
    lild_seq = 0
    iki_seq = 0
    rimi_seq = 0
    norfa_seq = 0

    def __init__(self):
        self.init_dirs()
    
    def init_dirs(self):
        """
        Initializes the required directories if they do not exist.
        """
        required_dirs = [HTML_DIR, PARSED_DIR]
        required_dirs.extend([os.path.join(PARSED_DIR, subdir) for subdir in SM_DIRS.values()])

        for dir_path in required_dirs:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

    def process_item(self, item, spider):
        if isinstance(item, MaximaHtmlItem):
            self.store_html_maxima(item)
        elif isinstance(item, MaximaProductItem):
            parsed_dir = os.path.join(PARSED_DIR, SM_DIRS["MAXIMA"], self.CURRENT_DATE_DIR)
            if not os.path.exists(parsed_dir):
                os.mkdir(parsed_dir)
            self.store_parsed_maxima(item, parsed_dir, self.maxima_seq)
            self.maxima_seq += 1
            return item

    def store_html_maxima(self, item):
        page_num = item["page_num"]
        html = item["html"]
        html_path = Path(HTML_DIR) / SM_DIRS["MAXIMA"] / self.CURRENT_DATE_DIR / f"{page_num}.html"
        html_path.parent.mkdir(parents=True, exist_ok=True)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)

    def store_parsed_maxima(self, item, parsed_dir, seq):
        parsed_path = Path(PARSED_DIR) / SM_DIRS["MAXIMA"] / self.CURRENT_DATE_DIR / f"{self.maxima_seq}.json"
        parsed_path.parent.mkdir(parents=True, exist_ok=True)
        with open(parsed_path, 'w', encoding="utf-8") as fp:
            json.dump(dict(item), fp, indent=4, ensure_ascii=False)
