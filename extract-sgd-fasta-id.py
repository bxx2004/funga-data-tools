import os
import sys
from tqdm import tqdm


def load_file(input_path, output_path):
    # First pass - count lines for progress bar
    try:
        with open(input_path, "r", encoding='utf-8') as f:
            total_lines = sum(1 for _ in f)
    except IOError as e:
        print(f"Error reading input file: {e}")
        return

    # Collect unique IDs with progress bar
    ids = set()
    try:
        with open(input_path, "r", encoding='utf-8') as input_file:
            for line in tqdm(input_file, total=total_lines, desc="Processing lines"):
                if line.startswith(">"):  # Common FASTA header indicator
                    line = line[1:].split()[0]  # Take the first part after >
                elif "SGD1:" in line:  # Your specific case
                    line = line.replace("SGD1:", "").strip()
                else:
                    continue
                ids.add(line)
    except IOError as e:
        print(f"Error during processing: {e}")
        return

    # Write output
    try:
        with open(f"{output_path}.id", "w", encoding='utf-8') as output_file:
            for id in tqdm(ids, desc="Writing IDs"):
                output_file.write(f"{id}\n")
    except IOError as e:
        print(f"Error writing output file: {e}")
        return

    print(f"\nSuccessfully extracted {len(ids)} unique IDs to {output_path}.id")


if __name__ == '__main__':
    if len(sys.argv) == 3:
        input_path = sys.argv[1]
        output_path = sys.argv[2]

        if not os.path.exists(input_path):
            print(f"Error: Input file '{input_path}' not found")
            sys.exit(1)

        load_file(input_path, output_path)
    else:
        print("Usage: extract-sgd-fasta-id.py <input-file> <output-file>")
        print("Example:")
        print("  extract-sgd-fasta-id.py zfin.fasta zfin")
        sys.exit(1)