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
    phenotype_dir = os.path.join(path,"gene-phenotype")
    print("开始执行gene mapping,请耐心等待...")
    for gene_file in os.listdir(gene_dir):
        renumber_gene(os.path.join(gene_dir, gene_file))
    print("开始执行gene-gene mapping,请耐心等待...")
    for gene_gene_file in os.listdir(gene_gene_dir):
        renumber_gene_gene(os.path.join(gene_gene_dir, gene_gene_file))
    print("开始执行gene-phenotype mapping,请耐心等待...")
    for phenotype_file in os.listdir(phenotype_dir):
        renumber_phenotype(os.path.join(phenotype_dir, phenotype_file))
    print("开始执行mapping输出...")
    with open(output + "/mapping.json","a") as f:
        out = {}
        for k,v in mapping.items():
            out[k] = list(v)
        f.write(json.dumps(out))
    print("程序执行完成...")

def inMap(gene:str):
    for value in mapping.values():
        if gene in value:
            return True
    return False

def renumber_gene(gene_file:str):
    print("完成:" + gene_file)
    with open(gene_file,"r") as f:
        arr = json.loads(f.read())
        for obj in arr:
            source_id = obj["source"]["id"]
            a = generate_id()
            mapping[a] = {source_id}
            if obj["symbol"]:
                mapping[a].add(obj["symbol"])
            for i in obj["other_name"]:
                if i:
                    mapping[a].add(i)

def renumber_gene_gene(file:str):
    print("完成:" + file)
    with open(file,"r") as f:
        arr = json.loads(f.read())
        for obj in arr:
            source_gene1 = obj["source"]["gene1"]
            source_gene2 = obj["source"]["gene2"]
            if not inMap(source_gene1):
                mapping[generate_id()] = {source_gene1}
            if not inMap(source_gene2):
                mapping[generate_id()] = {source_gene2}


def renumber_phenotype(file:str):
    print("完成:" + file)
    with open(file,"r") as f:
        arr = json.loads(f.read())
        for obj in arr:
            source_gene = obj["source"]["gene"]
            if not inMap(source_gene):
                mapping[generate_id()] = {source_gene}

def generate_id():
    global index
    index = index + 1
    #F(G|S)(FChar1|GChar1)(GChar3|SChar3){NUMBER}
    return f"F{name.upper()}{index}"

name = ""
path = ""
output = ""

if __name__ == '__main__':
    if len(sys.argv) == 4:
        name = sys.argv[1]
        path = sys.argv[2]
        output = sys.argv[3]
        loadFile()
    else:
        print("Usage: renumber.py <name> <input-path> <output-path>")
        print("Example:")
        print("  renumber.py DRER zfin zfin")