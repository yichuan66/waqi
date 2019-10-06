import uuid
import datetime
from shared_utils import get_date_str, FileContract

class WaqiPipelineContextManager:
    def __init__(self):
        self._root_folder = '/home/yichuan33/waqi/data/'

    def download_output_contract(self):
        return FileContract(
            self._root_folder + 'download/',
            True,
            ['data_downloaded.csv'])

    def transform_output_contract(self):
        return FileContract(
            self._root_folder + 'transform/',
            True,
            ['data_transformed.csv'])

class WaqiDagManager:
    def __init__(self, 
                 input_file_contract = None,
                 output_file_contract = None,
                 workspace_root_folder = None):
        self.workspace_root_folder = workspace_root_folder
        self.input_file_contract = input_file_contract
        self.output_file_contract = output_file_contract

class WaqiDownloadDagManager(WaqiDagManager):    
    def __init__(self, output_file_contract):
        WaqiDagManager.__init__(self, 
                                input_file_contract=None,
                                output_file_contract=output_file_contract,
                                workspace_root_folder=None)
        self.output_file_path_list = output_file_contract.create_new_file_list()
    
    def data_path_output(self):
        return self.output_file_path_list[0]

    def token(self):
        return '3c7c262efbfad0c1d3921f5a3884987c614a1557'

class WaqiTransformDagManager(WaqiDagManager):
    def __init__(self, input_file_contract, output_file_contract):
        WaqiDagManager.__init__(self, 
                                input_file_contract=input_file_contract,
                                output_file_contract=output_file_contract,
                                workspace_root_folder=None)
        self.input_file_path_list = input_file_contract.get_latest_file_list()
        
        self.output_file_path_list = output_file_contract.create_new_file_list()
            
    def data_path_input(self):
        return self.input_file_path_list[0]

    def data_path_output(self):
        return self.output_file_path_list[0]
        