import json
import aiohttp
import asyncio
import csv
import os

from waqi_schema_helper import WaqiSchemaHelper

class WaqiDownloader:

    def __init__(self, token):
        self.token = token

    def download_waqi_data(self):
        response = self._fetch_response(0, 300)
        result = [WaqiSchemaHelper.parse_waqi_json_packet_to_csv_row(item) 
                  for item in response]   
        result = [item for item in result if item]
        return result

    def write_result(self, result, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w+', newline='') as csvfile:
            result_writer = csv.writer(csvfile,
                                       delimiter=',',
                                       quotechar='\"',
                                       quoting=csv.QUOTE_MINIMAL)
            result_writer.writerow(WaqiSchemaHelper.schema)
            result_writer.writerows(result)

    def _fetch_response(self, start, end):
        block_size = 500
        result = []
        loop = asyncio.get_event_loop()
        while start < end:
            block_start = start
            if end - start > block_size:
                block_end = block_start + block_size
            else:
                block_end = end
            start += block_size
            future = asyncio.ensure_future(self._fetch_response_in_block(block_start, block_end))
            result += loop.run_until_complete(future)     
        loop.close()   
        result = [json.loads(item) for item in result]
        return result

    async def _fetch_response_in_block(self, start, end):
        tasks = []
        async with aiohttp.ClientSession() as session:        
            for idx in range(start, end):
                task = asyncio.ensure_future(self._get_waqi_api_json_response(session, idx))
                tasks.append(task)
            return await asyncio.gather(*tasks)

    async def _get_waqi_api_json_response(self, session, idx):
        url = self._get_waqi_data_url_by_index(idx)
        async with session.get(url) as response:
            return await response.read()

    def _get_waqi_data_url_by_index(self, idx):
        return self._root_url() + '@' + str(idx) + '/?token=' + self.token

    def _root_url(self):
        return "https://api.waqi.info/feed/"
