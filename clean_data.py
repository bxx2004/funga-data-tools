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
    os.makedirs(os.path.join(path,f"{output}/gene"))
    os.makedirs(os.path.join(path,f"{output}/gene-gene"))
    os.makedirs(os.path.join(path,f"{output}/gene-phenotype"))

def loadFile():
    global mapping
    try_create_dir()
    gene_dir = os.path.join(path,"gene")
    gene_gene_dir = os.path.join(path,"gene-gene")
    phenotype_dir = os.path.join(path,"gene-phenotype")
    clean(gene_dir,"gene")
    clean(gene_gene_dir,"gene-gene")
    clean(phenotype_dir,"gene-phenotype")

def clean(dir,type):
    gene_cache = set([])
    for gf in os.listdir(dir):
        out_cache = []
        gene_arr = json.loads(open(os.path.join(dir,gf),'r').read())
        for gene in gene_arr:
            if get_sha256(str(gene)) not in gene_cache:
                gene_cache.add(get_sha256(str(gene)))
                out_cache.append(gene)
        with open(os.path.join(path,f"{output}/{type}/" + gf),'w') as f:
            f.write(json.dumps(out_cache))

if __name__ == '__main__':
    if len(sys.argv) == 3:
        path = sys.argv[1]
        output = sys.argv[2]
        loadFile()
    else:
        print("Usage: clean_data.py <input-path> <output-path>")
        print("Example:")
        print("  clean_data.py zfin zfin")