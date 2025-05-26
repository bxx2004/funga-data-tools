import json
import sys
from concurrent.futures import ThreadPoolExecutor
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from tqdm import tqdm

import configure


def validate_args():
    if len(sys.argv) != 3:
        raise Exception("Usage: embedding.py <FileName> <Type>")
    return sys.argv[1], sys.argv[2]


def setup_http_session():
    session = requests.Session()
    retry = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry, pool_connections=100, pool_maxsize=100)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def get_embedding(session, text: str, model: str) -> list[float]:
    url = configure.embedding_url
    payload = {"model": model, "prompt": text}
    try:
        response = session.post(url, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()["embedding"]
    except Exception as e:
        print(f"Error getting embedding for model {model}: {str(e)}")
        return []


def process_gene_objects(session, objects, show_progress=True):
    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []

        # Pre-submit all tasks
        for obj in objects:
            future_dna = executor.submit(
                get_embedding, session, obj["dna_sequence"], "dnatest"
            )
            future_ploy = executor.submit(
                get_embedding, session, obj["polypeptide_sequence"], "ploytest"
            )
            future_desc = executor.submit(
                get_embedding, session, obj["description"], "mxbai-embed-large"
            )
            futures.append((obj, future_dna, future_ploy, future_desc))

        # Process results as they complete
        for obj, future_dna, future_ploy, future_desc in (
                tqdm(futures, desc="Processing genes", unit="gene")
                if show_progress else futures
        ):
            results.append({
                "funga_id": obj["funga_id"],
                "symbol": obj["symbol"],
                "name": obj["name"],
                "other_id": obj["other_id"],
                "description": obj["description"],
                "type": obj["type"],
                "source": obj["source"],
                "dna_sequence": obj["dna_sequence"],
                "polypeptide_sequence": obj["polypeptide_sequence"],
                "dna_sequence_vector": future_dna.result(),
                "polypeptide_sequence_vector": future_ploy.result(),
                "description_vector": future_desc.result(),
            })
    return results


def process_gene_phenotype_objects(session, objects, show_progress=True):
    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []

        for obj in objects:
            # Handle reference field if present
            phenotype = obj["phenotype"]
            if "reference" in phenotype:
                phenotype["references"] = phenotype["reference"]
                del phenotype["reference"]

            future = executor.submit(
                get_embedding, session, phenotype["description"], "mxbai-embed-large"
            )
            futures.append((obj, future))

        for obj, future in (
                tqdm(futures, desc="Processing gene-phenotypes", unit="item")
                if show_progress else futures
        ):
            phenotype = obj["phenotype"]
            results.append({
                "gene": obj["source"]["gene"],
                "phenotype": phenotype["description"],
                "source": obj["source"],
                "references": phenotype.get("references", []),
                "phenotype_ontology": phenotype.get("phenotype_ontology", ""),
                "phenotype_ontology_qualifier": phenotype.get("phenotype_ontology_qualifier", ""),
                "phenotype_vector": future.result(),
            })
    return results


def process_ontology_objects(session, objects, obj_type, show_progress=True):
    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []

        for obj in objects:
            future = executor.submit(
                get_embedding, session, obj["description"], "mxbai-embed-large"
            )
            futures.append((obj, future))

        for obj, future in (
                tqdm(futures, desc=f"Processing {obj_type}", unit="item")
                if show_progress else futures
        ):
            result = {
                "ontology_id": obj["ontologyId"],
                "name": obj["name"],
                "upstream": obj["upstream"],
                "description": obj["description"],
                "downstream": obj["downstream"],
                "description_vector": future.result(),
            }
            if obj_type == "phenotype-ontology":
                result["qualifiers"] = obj.get("qualifiers", [])
            results.append(result)
    return results


def main():
    file_name, obj_type = validate_args()

    # Load data
    with open(file_name, "r") as f:
        data = json.load(f)

    print(f"Loaded data: {len(data) if isinstance(data, list) else len(data.get('datas', []))} items")

    # Setup HTTP session
    session = setup_http_session()

    # Process based on type
    if obj_type == "gene":
        results = process_gene_objects(session, data)
    elif obj_type == "gene-phenotype":
        results = process_gene_phenotype_objects(session, data)
    elif obj_type == "phenotype-ontology":
        results = process_ontology_objects(session, data["datas"], obj_type)
    elif obj_type == "phenotype-ontology-qualifier":
        results = process_ontology_objects(session, data["datas"], obj_type)
    else:
        raise ValueError(f"Unknown type: {obj_type}")

    # Save results
    output_file = f"{file_name}.emb"
    with open(output_file, "w") as f:
        json.dump(results, f)

    print(f"Saved embeddings to {output_file}")


if __name__ == "__main__":
    main()