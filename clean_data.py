import json
import os
import sys
import hashlib
from tqdm import tqdm
from multiprocessing import Pool, cpu_count
import functools


def get_sha256(input_str):
    """Generate SHA256 hash for input string."""
    return hashlib.sha256(input_str.encode('utf-8')).hexdigest()


def try_create_dir(output):
    """Create output directories if they don't exist."""
    os.makedirs(f"{output}/gene", exist_ok=True)
    os.makedirs(f"{output}/gene-gene", exist_ok=True)
    os.makedirs(f"{output}/gene-phenotype", exist_ok=True)


def process_file(file_path, output_dir, cache):
    """Process a single file to remove duplicates."""
    try:
        with open(file_path, 'r') as f:
            gene_arr = json.load(f)

        out_cache = []
        seen_hashes = set()

        for gene in gene_arr:
            gene_hash = get_sha256(str(gene))
            if gene_hash not in cache and gene_hash not in seen_hashes:
                seen_hashes.add(gene_hash)
                out_cache.append(gene)

        output_path = os.path.join(output_dir, os.path.basename(file_path))
        with open(output_path, 'w') as f:
            json.dump(out_cache, f)

        return seen_hashes
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return set()


def clean_directory(input_dir, output_dir, data_type):
    """Process all files in a directory to remove duplicates."""
    cache = set()
    files = [os.path.join(input_dir, f) for f in os.listdir(input_dir)
             if os.path.isfile(os.path.join(input_dir, f))]

    # Process files in parallel
    with Pool(processes=cpu_count()) as pool:
        results = list(tqdm(
            pool.imap(functools.partial(process_file, output_dir=output_dir, cache=cache), files),
            total=len(files),
            desc=f"Processing {data_type} files"
        ))

        # Update cache with all hashes from all files
        for hashes in results:
            cache.update(hashes)


def load_files(path, output):
    """Main function to process all data directories."""
    try_create_dir(output)

    directories = {
        "gene": os.path.join(path, "gene"),
        "gene-gene": os.path.join(path, "gene-gene"),
        "gene-phenotype": os.path.join(path, "gene-phenotype")
    }

    for data_type, input_dir in directories.items():
        if os.path.exists(input_dir):
            clean_directory(
                input_dir,
                os.path.join(output, data_type),
                data_type
            )
        else:
            print(f"Warning: Directory {input_dir} does not exist")


if __name__ == '__main__':
    if len(sys.argv) == 3:
        path = sys.argv[1]
        output = sys.argv[2]
        load_files(path, output)
    else:
        print("Usage: clean_data.py <input-path> <output-path>")