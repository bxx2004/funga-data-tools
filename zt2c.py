import json
import os

dir = "./zhangtao"
mapping = json.loads(open("./SGD/sgd/mapping.json", "r").read())
"""
{
  "source": {
    "name": "NCBI",
    "link": "https://www.ncbi.nlm.nih.gov/bioproject/PRJEB11515",
    "gene": "S000000071"
  },
  "extra": {
    "group": "双基因敲除组(URA3,MET15knockout)_vs_单基因敲除组(URA3knockout).txt"
  },
  "phenotype": {
    "description": "Covalent modification of a specified RNA; type of modification specified.",
    "reference": [
      "https://pubmed.ncbi.nlm.nih.gov/27572163"
    ],
    "phenotype_ontology": "APO:0000271",
    "phenotype_ontology_qualifier": ""
  }
}
"""
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