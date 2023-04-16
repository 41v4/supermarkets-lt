import datetime
import os
import re


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
    
def is_weight_str_valid(value):
    find_strs = [" kg", " g", " l", " rit.", " ml"]
    if any([value.strip().endswith(i) for i in find_strs]):
        return True
    return False

def extract_lidl_dates(value):
    """
    Extracts start and end dates from strings like these:
    'Nuo 4.10.'
    '4.10. - 4.16.'
    """
    dates = {
        "start_date": None,
        "end_date": None,
    }
    if not value:
        return dates
    # regular expression pattern to match date formats
    pattern = r'(\d{1,2}\.\d{1,2}\.)\s*-\s*(\d{1,2}\.\d{1,2}\.)?(\d{4})?'

    # find all matches of date formats in the text
    matches = re.findall(pattern, value.strip())
    for m in matches:
        # parse the start date
        start_date = datetime.datetime.strptime(m[0], '%m.%d.')
        start_date_str = start_date.strftime("%Y-%m-%d")
        
        # check if there's an end date in the match
        if m[1]:
            end_date = datetime.datetime.strptime(m[1], '%m.%d.')
            end_date_str = end_date.strftime("%Y-%m-%d")
        else:
            # if no end date, use the start date
            end_date = start_date
            end_date_str = None
        
        # check if there's a year in the match
        if m[2]:
            # if year is specified, use it for start and end dates
            if end_date:
                end_date = end_date.replace(year=int(m[2]))
                end_date_str = end_date.strftime("%Y-%m-%d")
            start_date = start_date.replace(year=int(m[2]))
            start_date_str = start_date.strftime("%Y-%m-%d")
        else:
            # if no year is specified, use current year
            now = datetime.datetime.now()
            if end_date:
                end_date = end_date.replace(year=now.year)
                end_date_str = end_date.strftime("%Y-%m-%d")
            start_date = start_date.replace(year=now.year)
            start_date_str = start_date.strftime("%Y-%m-%d")
        
        # append the start and end dates as a tuple to the list of dates
        if start_date_str and end_date_str:
            if start_date < end_date:
                dates["start_date"] = start_date_str
                dates["end_date"] = end_date_str
            elif start_date == end_date:
                dates["start_date"] = start_date_str
                dates["end_date"] = None
        elif start_date_str and not end_date_str:
            dates["start_date"] = start_date_str
            dates["end_date"] = None
    
    # return the list of dates
    return dates