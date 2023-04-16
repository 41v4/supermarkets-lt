import datetime
import os


def is_valid_date_arg(date_arg):
    try:
        datetime.datetime.strptime(date_arg, '%Y_%m_%d')
        return True
    except ValueError:
        return False
    
def is_html_dir_exist(html_dir):
    if os.path.exists(html_dir):
        return True
    return False

def is_discount_valid(value):
    cleaned_value = value.replace("%", "").strip()
    try:
        int(cleaned_value)
        return True
    except ValueError:
        return False

def is_price_valid(value):
    cleaned_value = value.replace("€", "").strip()
    try:
        float(cleaned_value)
        return True
    except ValueError:
        return False