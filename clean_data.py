import json
import os
import sys

path = ""
output = ""
mapping = {}

def try_create_dir():
    os.makedirs(os.path.join(path,"clean_data/gene"))
    os.makedirs(os.path.join(path,"clean_data/gene-gene"))
    os.makedirs(os.path.join(path,"clean_data/gene-phenotype"))

def loadFile():
    global mapping
    try_create_dir()
    gene_dir = os.path.join(path,"gene")
    gene_gene_dir = os.path.join(path,"gene-gene")
    phenotype_dir = os.path.join(path,"phenotype")
    clean(gene_dir,"gene")
    clean(gene_gene_dir,"gene-gene")
    clean(phenotype_dir,"gene-phenotype")

def clean(dir,type):
    gene_cache = []
    for gf in os.listdir(dir):
        out_cache = []
        gene_arr = json.loads(open(gf,'r').read())
        for gene in gene_arr:
            if gene not in gene_cache:
                gene_cache.append(gene)
                out_cache.append(gene)
        with open(os.path.join(path,f"clean_data/{type}/" + gf),'w') as f:
            f.write(json.dumps(out_cache))

if __name__ == '__main__':
    if len(sys.argv) == 2:
        path = sys.argv[0]
        output = sys.argv[1]
        loadFile()
    else:
        print("Usage: clean_data.py <input-path> <output-path>")
        print("Example:")
        print("  clean_data.py zfin zfin")