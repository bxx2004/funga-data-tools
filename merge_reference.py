import json
import os
import sys
import hashlib



path = ""
output = ""
mapping = {}



def get_sha256(input_str):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(input_str.encode('utf-8'))
    sha256_value = sha256_hash.hexdigest()
    return sha256_value

def try_create_dir():
    os.makedirs(f"{output}/gene-gene")
    os.makedirs(f"{output}/gene-phenotype")

def loadFile():
    global mapping
    try_create_dir()
    gene_gene_dir = os.path.join(path,"gene-gene")
    phenotype_dir = os.path.join(path,"gene-phenotype")
    merge_gene_gene(gene_gene_dir)
    merge_gene_phenotype(phenotype_dir)

def get_gg_unique_id(obj):
    return get_sha256(obj['source']['gene1'] + obj['source']['gene2'] + obj['type'])

def get_gp_unique_id(obj):
    return get_sha256(obj['source']['gene'] + obj['phenotype']['description'])

def split_dict_by_count(dictionary, count):
    sub_dicts = []
    keys = list(dictionary.keys())
    total_keys = len(keys)

    for i in range(0, total_keys, count):
        sub_dict = {k: dictionary[k] for k in keys[i:i + count]}
        sub_dicts.append(sub_dict)

    return sub_dicts
index = 0
def generate_id():
    global index
    index += 1
    return f"{index}.json"

def merge_gene_gene(dir):
    cache = dict()
    out_dir = f"{output}/gene-gene"
    for file in os.listdir(dir):
        print(os.path.join(dir,file))
        with open(os.path.join(dir,file),"r") as arr_file:
            arr = json.loads(arr_file.read())
            for obj in arr:
                if get_gg_unique_id(obj) in cache.keys():
                    if "reference" in obj:
                        cache[get_gg_unique_id(obj)]['reference'].extend(obj['reference'])
                    else:
                        cache[get_gg_unique_id(obj)]['reference'].extend(obj['references'])
                else:
                    if "references" in obj:
                        obj["reference"] = obj['references']
                        obj.pop("references")
                    cache[get_gg_unique_id(obj)] = obj


    for dic in split_dict_by_count(cache, 1000):
        gs = []
        for value in dic.values():
            gs.append(value)
        with open(os.path.join(out_dir,generate_id()),"w") as out_file:
            out_file.write(json.dumps(gs))

def merge_gene_phenotype(dir):
    cache = dict()
    out_dir = f"{output}/gene-phenotype"
    for file in os.listdir(dir):
        with open(os.path.join(dir,file),"r") as arr_file:
            arr = json.loads(arr_file.read())
            for obj in arr:
                if get_gp_unique_id(obj) in cache.keys():
                    cache[get_gp_unique_id(obj)]['phenotype']['reference'].extend(obj['phenotype']['reference'])
                else:
                    cache[get_gp_unique_id(obj)] = obj
    for dic in split_dict_by_count(cache, 1000):
        gs = []
        for value in dic.values():
            gs.append(value)
        with open(os.path.join(out_dir,generate_id()),"w") as out_file:
            out_file.write(json.dumps(gs))

if __name__ == '__main__':
    if len(sys.argv) == 3:
        path = sys.argv[1]
        output = sys.argv[2]
        loadFile()
    else:
        print("Usage: merge_reference.py <input-path> <output-path>")
        print("Example:")
        print("  merge_reference.py zfin zfin")
