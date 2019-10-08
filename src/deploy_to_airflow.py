import shutil
import os

root_path = "/home/yichuan33"
src_root_path = root_path + "/waqi/src/"
dst_root_path = root_path + "/airflow/dags/waqi_dags/"

src_list = [
    "waqi_downloader.py",
    "waqi_dag_managers.py",
    "waqi_pipeline_jobs.py",
    "waqi_schema_helper.py",
    "shared_utils.py",
]

dag_src_root_path = src_root_path + "dags/"
dag_list = [   
    "waqi_download_dag.py"
]

if os.path.exists(dst_root_path):
    shutil.rmtree(dst_root_path)
os.mkdir(dst_root_path)

for file in src_list:
    src = src_root_path + file
    dst = dst_root_path + file
    shutil.copyfile(src, dst)

for file in dag_list:
    src = dag_src_root_path + file
    dst = dst_root_path + file
    shutil.copyfile(src, dst)

init_py_file = dst_root_path + '__init__.py'
f = open(init_py_file, 'w+')
f.truncate()

import git
repo = git.Repo(src_root_path, search_parent_directories=True)
sha = repo.head.object.hexsha
version_file = dst_root_path + 'version.txt'
f = open(version_file, 'w+')
f.truncate()
f.write(sha)