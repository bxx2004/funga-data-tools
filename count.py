import json
import os
import sys
from tqdm import tqdm


def load_file(input_path):
    """Load and count entries from gene-related JSON files with progress tracking."""
    directories = {
        "gene": os.path.join(input_path, "gene"),
        "gene-gene": os.path.join(input_path, "gene-gene"),
        "gene-phenotype": os.path.join(input_path, "gene-phenotype")
    }

    results = {}

    for name, directory in directories.items():
        total_files = 0
        total_entries = 0

        # First pass: count total files for progress bar
        if os.path.exists(directory):
            file_list = [f for f in os.listdir(directory) if f.endswith('.json')]
            total_files = len(file_list)

            # Second pass: process files with progress bar
            with tqdm(total=total_files, desc=f"Processing {name}", unit="file") as pbar:
                for filename in file_list:
                    filepath = os.path.join(directory, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            total_entries += len(data)
                    except (json.JSONDecodeError, UnicodeDecodeError) as e:
                        print(f"\nError processing {filepath}: {e}", file=sys.stderr)
                    pbar.update(1)

        results[name] = total_entries

    # Print results
    for name, count in results.items():
        print(f"{name}: {count:,}")


if __name__ == '__main__':
    if len(sys.argv) == 2:
        path = sys.argv[1]
        if not os.path.exists(path):
            print(f"Error: Path '{path}' does not exist", file=sys.stderr)
            sys.exit(1)
        load_file(path)
    else:
        print("Usage: count.py <input-path>")
        print("Example:")