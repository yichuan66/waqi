import uuid
import datetime

class WaqiPipelineManager:    
    def __init__(self):
        self.run_date = datetime.datetime.now()
    
    def data_path_downloaded(self):
        return self.root_url() + 'data_downloaded.csv'

    def data_path_cleaned(self):
        return self.root_url() + 'data_cleaned.csv'

    def root_url(self):
        date_str = self.run_date.strftime('%Y-%m-%d_%H_%M_%S_%f')[:-3]
        return self.root_url_base() + date_str + '/'

    def root_url_base(self):
        return '/home/yichuan33/waqi/data/'

    def token(self):
        return '3c7c262efbfad0c1d3921f5a3884987c614a1557'