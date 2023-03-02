import json
import os

dataset_location = os.getcwd()+'/src/main/resources/dataset.json'
f = open(dataset_location)
data = json.load(f)
print(data)