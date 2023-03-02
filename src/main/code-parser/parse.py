import ast
import os
from pathlib import Path

def clone_repo(repo_url):
    clone_path  = "./tmp/" 
    for f in os.scandir(clone_path):
        if f.path.split("/")[-1] != repo_url.split("/")[-1]:
            print("Cloning repository: "+f.path)
            clone = "git clone "+repo_url+".git" 
            # os.system("sshpass -p your_password ssh user_name@your_localhost")
            os.chdir(clone_path) # Specifying the path where the cloned project needs to be copied
            os.system(clone) # Cloning
        else:
            print("Repository already cloned!")
    
def parse_repo(repo_url):
    clone_repo(repo_url)
    repo_dir = "./tmp/"+repo_url.split("/")[-1]
    pyfile_list = get_subdir_filepath(repo_dir)
    for file in pyfile_list[:1]:
        parse_pyfile(file.__str__())
    return

def get_subdir_filepath(repo_dir):
    result = list(Path("./tmp/").rglob("*.py"))
    return result

def parse_pyfile(pyfile_path):
    print(pyfile_path)

