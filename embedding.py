import json
import sys

if len(sys.argv) == 3:
    file_name = sys.argv[1]
    type = sys.argv[2]
else:
    raise Exception("Usage: embedding.py <FileName> <Type>")

result = set()

def get_embedding(text: str) -> list[float]:
    import requests
    url = "http://localhost:11434/api/embeddings"
    payload = {
        "model": "mxbai-embed-large",
        "prompt": text
    }
    response = requests.post(url, json=payload)
    return response.json()["embedding"]

def get_dna_embedding(text: str) -> list[float]:
    import requests
    url = "http://localhost:11434/api/embeddings"
    payload = {
        "model": "mxbai-embed-large",
        "prompt": text
    }
    response = requests.post(url, json=payload)
    return response.json()["embedding"]

def get_ploy_embedding(text: str) -> list[float]:
    import requests
    url = "http://localhost:11434/api/embeddings"
    payload = {
        "model": "mxbai-embed-large",
        "prompt": text
    }
    response = requests.post(url, json=payload)
    return response.json()["embedding"]

with open(file_name, "r") as f:
    arr = json.loads(f.read())
    match type:
        case "gene":
            for obj in arr:
                result.add({
                    "funga_id": obj["funga_id"],
                    "symbol": obj["symbol"],
                    "name": obj["name"],
                    "other_id": obj["other_id"],
                    "description": obj["description"],
                    "type": obj["type"],
                    "source": obj["source"],
                    "dna_sequence": obj["dna_sequence"],
                    "polypeptide_sequence": obj["polypeptide_sequence"],
                    "dna_sequence_vector": get_dna_embedding(obj["dna_sequence"]),
                    "polypeptide_sequence_vector": get_ploy_embedding(obj["polypeptide_sequence"]),
                    "description_vector": get_embedding(obj["description"]),
                })
        case "gene-phenotype":
            for obj in arr:
                result.add({
                    "gene": obj["source"]["gene"],
                    "phenotype": obj["phenotype"]["description"],
                    "source": obj["source"],
                    "references": obj["phenotype"]["references"],
                    "phenotype_ontology": obj["phenotype"]["phenotype_ontology"],
                    "phenotype_ontology_qualifier": obj["phenotype"]["phenotype_ontology_qualifier"],
                    "phenotype_vector": get_embedding(obj["phenotype"]["description"])
                })

        case "phenotype-ontology":
            for obj in arr["datas"]:
                result.add({
                    "ontology_id": obj["ontologyId"],
                    "name": obj["name"],
                    "upstream": obj["upstream"],
                    "description": obj["description"],
                    "downstream": obj["downstream"],
                    "qualifiers": obj["qualifiers"],
                    "description_vector": get_embedding(obj["description"])
                })

        case "phenotype-ontology-qualifier":
            for obj in arr["datas"]:
                result.add({
                    "ontology_id": obj["ontologyId"],
                    "name": obj["name"],
                    "upstream": obj["upstream"],
                    "description": obj["description"],
                    "downstream": obj["downstream"],
                    "description_vector": get_embedding(obj["description"])
                })
data_dir = file_name + ".emb"
with open(data_dir,"w") as f:
    f.write(json.dumps(list(result)))