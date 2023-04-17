import datetime
import json
import os
from pathlib import Path

from itemadapter import ItemAdapter

from sm_scrapy.items import MaximaHtmlItem, MaximaProductItem, LidlHtmlItem, LidlProductItem
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
            self.store_html_maxima(item, self.maxima_seq)
            self.maxima_seq += 1
        elif isinstance(item, MaximaProductItem):
            self.store_parsed_maxima(item)
            self.maxima_seq += 1
            return item
        elif isinstance(item, LidlHtmlItem):
            self.store_html_lidl(item, self.lild_seq)
            self.lild_seq += 1
        elif isinstance(item, LidlProductItem):
            self.store_parsed_lidl(item)

    def store_html_maxima(self, item, seq):
        html = item["html"]
        html_path = Path(HTML_DIR) / SM_DIRS["MAXIMA"] / self.CURRENT_DATE_DIR / f"{seq}.html"
        html_path.parent.mkdir(parents=True, exist_ok=True)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)

    def store_parsed_maxima(self, item):
        fn_num = item["fn_num"]
        parsed_path = Path(PARSED_DIR) / SM_DIRS["MAXIMA"] / self.CURRENT_DATE_DIR / f"{fn_num}.json"
        parsed_path.parent.mkdir(parents=True, exist_ok=True)
        with open(parsed_path, 'w', encoding="utf-8") as fp:
            json.dump(dict(item), fp, indent=4, ensure_ascii=False)
    
    def store_html_lidl(self, item, seq):
        html = item["html"]
        html_path = Path(HTML_DIR) / SM_DIRS["LIDL"] / self.CURRENT_DATE_DIR / f"{seq}.html"
        html_path.parent.mkdir(parents=True, exist_ok=True)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)

    def store_parsed_lidl(self, item):
        fn_num = item["fn_num"]
        parsed_path = Path(PARSED_DIR) / SM_DIRS["LIDL"] / self.CURRENT_DATE_DIR / f"{fn_num}.json"
        parsed_path.parent.mkdir(parents=True, exist_ok=True)
        with open(parsed_path, 'w', encoding="utf-8") as fp:
            json.dump(dict(item), fp, indent=4, ensure_ascii=False)
