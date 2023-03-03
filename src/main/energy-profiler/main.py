import json
from pathlib import Path
from parse import *

dataset_location = Path.cwd().__str__()+'/src/main/resources/dataset.json'
f = open(dataset_location)
data = json.load(f)
repo_url = data[1]['repositories'][0]
parse_repo(repo_url)