import json
import os
import sys
import hashlib
from tqdm import tqdm
from typing import Dict, Any, List

path = ""
output = ""
mapping = {}


def get_sha256(input_str: str) -> str:
    """Generate SHA256 hash of input string."""
    return hashlib.sha256(input_str.encode('utf-8')).hexdigest()


def try_create_dir() -> None:
    """Create output directories if they don't exist."""
    os.makedirs(f"{output}/gene-gene", exist_ok=True)
    os.makedirs(f"{output}/gene-phenotype", exist_ok=True)


def loadFile() -> None:
    """Main function to load and process files."""
    global mapping
    try_create_dir()
    gene_gene_dir = os.path.join(path, "gene-gene")
    phenotype_dir = os.path.join(path, "gene-phenotype")

    print("Processing gene-gene relationships...")
    merge_gene_gene(gene_gene_dir)

    print("\nProcessing gene-phenotype relationships...")
    merge_gene_phenotype(phenotype_dir)


def get_gg_unique_id(obj: Dict[str, Any]) -> str:
    """Generate unique ID for gene-gene relationship."""
    return get_sha256(obj['source']['gene1'] + obj['source']['gene2'] + obj['type'])


def get_gp_unique_id(obj: Dict[str, Any]) -> str:
    """Generate unique ID for gene-phenotype relationship."""
    return get_sha256(obj['source']['gene'] + obj['phenotype']['description'])


def split_dict_by_count(dictionary: Dict[str, Any], count: int) -> List[Dict[str, Any]]:
    """Split dictionary into chunks of specified size."""
    return [dict(list(dictionary.items())[i:i + count])
            for i in range(0, len(dictionary), count)]


class FileIdGenerator:
    """Generator for sequential file IDs."""

    def __init__(self):
        self.index = 0

    def generate(self) -> str:
        self.index += 1
        return f"{self.index}.json"


def merge_gene_gene(dir_path: str) -> None:
    """Merge gene-gene relationship files."""
    cache: Dict[str, Dict[str, Any]] = {}
    out_dir = f"{output}/gene-gene"
    file_id_gen = FileIdGenerator()

    # Get all files with progress bar
    files = [f for f in os.listdir(dir_path) if f.endswith('.json')]

    for file in tqdm(files, desc="Processing files"):
        file_path = os.path.join(dir_path, file)
        try:
            with open(file_path, "r") as arr_file:
                arr = json.load(arr_file)
                for obj in arr:
                    obj_id = get_gg_unique_id(obj)

                    # Handle references consistently
                    if "references" in obj:
                        obj["reference"] = obj.pop("references")

                    if obj_id in cache:
                        cache[obj_id]['reference'].extend(obj.get('reference', []))
                    else:
                        cache[obj_id] = obj
        except Exception as e:
            print(f"\nError processing {file_path}: {str(e)}")
            continue

    # Write output in chunks with progress
    for chunk in tqdm(split_dict_by_count(cache, 1000), desc="Writing output"):
        output_data = list(chunk.values())
        output_file = os.path.join(out_dir, file_id_gen.generate())
        with open(output_file, "w") as out_file:
            json.dump(output_data, out_file)


def merge_gene_phenotype(dir_path: str) -> None:
    """Merge gene-phenotype relationship files."""
    cache: Dict[str, Dict[str, Any]] = {}
    out_dir = f"{output}/gene-phenotype"
    file_id_gen = FileIdGenerator()

    # Get all files with progress bar
    files = [f for f in os.listdir(dir_path) if f.endswith('.json')]

    for file in tqdm(files, desc="Processing files"):
        file_path = os.path.join(dir_path, file)
        try:
            with open(file_path, "r") as arr_file:
                arr = json.load(arr_file)
                for obj in arr:
                    obj_id = get_gp_unique_id(obj)
                    if obj_id in cache:
                        cache[obj_id]['phenotype']['reference'].extend(
                            obj['phenotype']['reference'])
                    else:
                        cache[obj_id] = obj
        except Exception as e:
            print(f"\nError processing {file_path}: {str(e)}")
            continue

    # Write output in chunks with progress
    for chunk in tqdm(split_dict_by_count(cache, 1000), desc="Writing output"):
        output_data = list(chunk.values())
        output_file = os.path.join(out_dir, file_id_gen.generate())
        with open(output_file, "w") as out_file:
            json.dump(output_data, out_file)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        path = sys.argv[1]
        output = sys.argv[2]
        loadFile()
    else:
        print("Usage: merge_reference.py <input-path> <output-path>")
        print("Example:")
        print("  merge_reference.py zfin zfin")