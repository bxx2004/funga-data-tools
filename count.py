import json
import os
import sys

path = ""

def loadFile():
    global mapping
    gene_dir = os.path.join(path,"gene")
    gene_gene_dir = os.path.join(path,"gene-gene")
    phenotype_dir = os.path.join(path,"gene-phenotype")
    count(gene_dir,"gene")
    count(gene_gene_dir,"gene-gene")
    count(phenotype_dir,"gene-phenotype")

def count(dir,type):
    size = 0
    for gf in os.listdir(dir):
        gene_arr = json.loads(open(os.path.join(dir,gf),'r').read())
        size += len(gene_arr)
    print(f"{type}: {size}")
if __name__ == '__main__':
    if len(sys.argv) == 2:
        path = sys.argv[1]
        loadFile()
    else:
        print("Usage: count.py <input-path>")
        print("Example:")
        print("  count.py zfin")