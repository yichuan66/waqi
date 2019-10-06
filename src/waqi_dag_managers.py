import uuid
import datetime
import os
from glob import glob
from shared_utils import get_date_str

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

class FileContract():
    def __init__(self, root_folder, use_versioned_subdir, filename_list):
        self.root_folder = root_folder
        self.use_versioned_subdir = use_versioned_subdir
        self.filename_list = filename_list

    def get_latest_file_list(self):
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
        