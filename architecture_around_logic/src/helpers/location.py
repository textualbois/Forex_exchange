import re


def location_is_valid(location):
    regex_lat = r'^(\+|-)?(?:90(?:(?:\.0{1,7})?)|(?:[0-9]|[1-8][0-9])(?:(?:\.[0-9]{1,7})?))$'
    regex_lon = r'^(\+|-)?(?:180(?:(?:\.0{1,7})?)|(?:[0-9]|[1-9][0-9]|1[0-7][0-9])(?:(?:\.[0-9]{1,7})?))$'
    if len(location) == 2:
        if re.match(regex_lat, location[0]) and re.match(regex_lon, location[1]):
            return True
    else:
        return False
