import json
import os
from parse import *

dataset_location = os.getcwd()+'/src/main/resources/dataset.json'
f = open(dataset_location)
data = json.load(f)
repo_url = data[1]['repositories'][0]
parse_repo(repo_url)