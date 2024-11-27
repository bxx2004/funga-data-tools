
import os
import sys

path = ""
output = ""
mapping = {}

def try_create_dir():
    os.makedirs(os.path.join(path,"transfer_data/gene"))
    os.makedirs(os.path.join(path,"transfer_data/gene-gene"))
    os.makedirs(os.path.join(path,"transfer_data/gene-phenotype"))

def loadFile():
    global mapping
    try_create_dir()
    gene_dir = os.path.join(path,"gene")
    gene_gene_dir = os.path.join(path,"gene-gene")
    phenotype_dir = os.path.join(path,"phenotype")


if __name__ == '__main__':
    if len(sys.argv) == 2:
        path = sys.argv[0]
        output = sys.argv[1]
        loadFile()
    else:
        print("Usage: transfer.py <input-path> <output-path>")
        print("Example:")
        print("  transfer.py zfin zfin")