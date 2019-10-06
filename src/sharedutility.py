def is_valid_latitude(item):
    if not is_float(item):
        return False
    else:
        val = float(item)
        return -90 <= val and 90 > val

def is_valid_longitude(item):
    if not is_float(item):
        return False
    else:
        val = float(item)
        return -180 <= val and 180 > val

def is_float(item):
    try:
        float(item)
        return True
    except ValueError:
        return False