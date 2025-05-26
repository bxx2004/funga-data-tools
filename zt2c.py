import json
import os

dir = "./zhangtao"
mapping = json.loads(open("SGD1/sgd/mapping.json", "r").read())

def find_id(name):
    for (key, value) in mapping.items():
        if name in value:
            return key
    return None

cache = []
for fname in os.listdir(dir):
    f_path = os.path.join(dir,fname)
    with open(f_path,'r',encoding="utf-8") as f:
        array = json.loads(f.read())
        for obj in array:
            obj["source"]["gene"] = find_id(obj["source"]["gene"])
        cache = cache + array

with open("./zhangtao.json",'w+') as out:
    out.write(json.dumps(cache))