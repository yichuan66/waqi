import datetime

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

def get_date_str(date):
    return date.strftime('%Y-%m-%d_%H_%M_%S_%f')[:-3]

class FileContract():
    def __init__(self, root_folder, use_versioned_subdir, filename_list):
        self.root_folder = root_folder
        self.use_versioned_subdir = use_versioned_subdir
        self.filename_list = filename_list

    def get_latest_file_list(self):
        import os
        from glob import glob
        base_folder = self.root_folder
        if self.use_versioned_subdir:
            dirs = glob(os.path.join(self.root_folder, "*", ""))
            base_folder = sorted(dirs)[-1]
        return [base_folder + item for item in self.filename_list]

    def create_new_file_list(self):
        base_folder = self.root_folder
        if self.use_versioned_subdir:
            base_folder += get_date_str(datetime.datetime.now()) + '/'
        return [base_folder + item for item in self.filename_list]