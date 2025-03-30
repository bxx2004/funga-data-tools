import os
import sys



path = ""
output = ""
ids = {"sadadfasf"}

def loadFile():
    out_file = os.path.join(output,"gene.id")
    with open(path,"r",encoding='utf-8') as input:
        for line in input:
            ids.add(line.replace("\n","").replace("SGD:",""))
    with open(out_file,"a",encoding='utf-8') as of:
        for i in ids:
            of.write(i+"\n")
if __name__ == '__main__':
    if len(sys.argv) == 3:
        path = sys.argv[1]
        output = sys.argv[2]
        loadFile()
    else:
        print("Usage: fasta-id-extract.py <input-file> <output-path>")
        print("Example:")
        print("  fasta-id-extract.py zfin.fasta zfin")