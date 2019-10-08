import csv
import os

from waqi_schema_helper import WaqiSchemaHelper
from waqi_downloader import WaqiDownloader

def download_raw_waqi_data(token, output_path):    
    helper = WaqiDownloader(token)
    result = helper.download_waqi_data()
    helper.write_result(result, output_path)

def filter_incomplete_row(input_path, output_path):
    data = []
    with open(input_path, 'r', newline='') as input_file:
        data_reader = csv.reader(input_file, delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
        for row in data_reader:
            data.append(row)
    
    if len(data) == 0:
        return
    
    header_row = data.pop(0)
    data = [row for row in data if WaqiSchemaHelper.is_valid_row(row)]

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w+', newline='') as output_file:
        data_writer = csv.writer(output_file, delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(header_row)
        data_writer.writerows(data)
