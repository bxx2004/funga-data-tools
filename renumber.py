import json
import os
import sys


index = 0
mapping = {}
def loadFile():
    global index
    index = 0
    gene_dir = os.path.join(path,"gene")
    gene_gene_dir = os.path.join(path,"gene-gene")
    phenotype_dir = os.path.join(path,"phenotype")
    print("开始执行gene mapping,请耐心等待...")
    for gene_file in os.listdir(gene_dir):
        renumber_gene(gene_file)
    print("开始执行gene-gene mapping,请耐心等待...")
    for gene_gene_file in os.listdir(gene_gene_dir):
        renumber_gene_gene(gene_gene_file)
    print("开始执行gene-phenotype mapping,请耐心等待...")
    for phenotype_file in os.listdir(phenotype_dir):
        renumber_phenotype(phenotype_file)
    print("开始执行mapping输出...")
    with open(output,"a") as f:
        f.write(json.dumps(mapping))
    print("程序执行完成...")

def inMap(gene:str):
    for value in mapping.values():
        if gene in value:
            return True
    return False

def renumber_gene(gene_file:str):
    with open(gene_file,"r") as f:
        arr = json.loads(f.read())
        for obj in arr:
            source_id = obj["source"]["id"]
            a = generate_id()
            mapping[a] = [source_id]
            mapping[a].append(obj["symbol"])
            mapping[a].append(obj["other_name"])

def renumber_gene_gene(file:str):
    with open(file,"r") as f:
        arr = json.loads(f.read())
        for obj in arr:
            source_gene1 = obj["source"]["gene1"]
            source_gene2 = obj["source"]["gene2"]
            if not inMap(source_gene1):
                mapping[generate_id()] = source_gene1
            if not inMap(source_gene2):
                mapping[generate_id()] = source_gene2


def renumber_phenotype(file:str):
    with open(file,"r") as f:
        arr = json.loads(f.read())
        for obj in arr:
            source_gene = obj["source"]["gene"]
            if not inMap(source_gene):
                mapping[generate_id()] = source_gene

def generate_id():
    global index
    index = index + 1
    return f"FUNGA-{name.upper()}-{index}"

name = ""
path = ""
output = ""

if __name__ == '__main__':
    if len(sys.argv) == 3:
        name = sys.argv[0]
        path = sys.argv[1]
        output = sys.argv[2]
        loadFile()
    else:
        print("Usage: renumber.py <name> <input-path> <output-path>")
        print("Example:")
        print("  renumber.py DRER zfin zfin/mapping.json")