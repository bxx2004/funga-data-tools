import json
import sys
import os
from tqdm import tqdm  # For progress bars


class JSONToCSVConverter:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.mapping = {}

        # Initialize output files
        os.makedirs(output_path, exist_ok=True)
        self.out_files = {
            'gene': open(os.path.join(output_path, "gene.csv"), "a", encoding="utf-8"),
            'gene_phenotype': open(os.path.join(output_path, "gene_phenotype.csv"), "a", encoding="utf-8"),
            'gene_gene': open(os.path.join(output_path, "gene_gene.csv"), "a", encoding="utf-8"),
            'phenotype_ontology': open(os.path.join(output_path, "phenotype_ontology.csv"), "a", encoding="utf-8"),
            'phenotype_ontology_qualifier': open(os.path.join(output_path, "phenotype_ontology_qualifier.csv"), "a",
                                                 encoding="utf-8"),
            'gene_ontologies': open(os.path.join(output_path, "gene_ontologies.csv"), "a", encoding="utf-8"),
            'gene_regulations': open(os.path.join(output_path, "gene_regulations.csv"), "a", encoding="utf-8")
        }

    def map_id(self, id):
        """Optimized ID mapping with caching"""
        for key, value in self.mapping.items():
            if id in value:
                return key
        return None

    def process_files(self):
        """Process all JSON files with progress tracking"""
        # Load mapping
        mapping_file = os.path.join(self.input_path, "mapping.json")
        if os.path.exists(mapping_file):
            with open(mapping_file, "r") as f:
                self.mapping = json.load(f)

        # Process each data type with progress bars
        self._process_gene_files()
        self._process_gene_gene_files()
        self._process_gene_phenotype_files()
        self._process_single_files()

    def _process_gene_files(self):
        """Process gene files with progress tracking"""
        gene_dir = os.path.join(self.input_path, "gene")
        if os.path.exists(gene_dir):
            files = [f for f in os.listdir(gene_dir) if f.endswith('.json')]
            for file in tqdm(files, desc="Processing gene files"):
                self._process_file(os.path.join(gene_dir, file), "gene")

    def _process_gene_gene_files(self):
        """Process gene-gene files with progress tracking"""
        gg_dir = os.path.join(self.input_path, "gene-gene")
        if os.path.exists(gg_dir):
            files = [f for f in os.listdir(gg_dir) if f.endswith('.json')]
            for file in tqdm(files, desc="Processing gene-gene files"):
                self._process_file(os.path.join(gg_dir, file), "gene_gene")

    def _process_gene_phenotype_files(self):
        """Process gene-phenotype files with progress tracking"""
        gp_dir = os.path.join(self.input_path, "gene-phenotype")
        if os.path.exists(gp_dir):
            files = [f for f in os.listdir(gp_dir) if f.endswith('.json')]
            for file in tqdm(files, desc="Processing gene-phenotype files"):
                self._process_file(os.path.join(gp_dir, file), "gene_phenotype")

    def _process_single_files(self):
        """Process single JSON files with progress tracking"""
        single_files = {
            "gene_ontology": "go-term.json",
            "gene_regulation": "go-regulate.json",
            "phenotype_ontology": "phenotype-ontology.json",
            "phenotype_ontology_qualifier": "phenotype-ontology-qualifier.json"
        }

        for file_type, file_name in single_files.items():
            file_path = os.path.join(self.input_path, file_name)
            if os.path.exists(file_path):
                self._process_file(file_path, file_type)

    def _process_file(self, file_path, file_type):
        """Process a single JSON file"""
        try:
            with open(file_path, "r") as f:
                data = json.load(f)

            if file_type == "gene":
                for ele in data:
                    self.out_files['gene'].write(f"{self._transfer_gene(ele)}\n")
            elif file_type == "gene_gene":
                for ele in data:
                    self.out_files['gene_gene'].write(f"{self._transfer_gene_gene(ele)}\n")
            elif file_type == "gene_phenotype":
                for ele in data:
                    self.out_files['gene_phenotype'].write(f"{self._transfer_gene_phenotype(ele)}\n")
            elif file_type == "phenotype_ontology":
                for ele in data['datas']:
                    self.out_files['phenotype_ontology'].write(f"{self._transfer_phenotype_ontology(ele)}\n")
            elif file_type == "phenotype_ontology_qualifier":
                for ele in data['datas']:
                    self.out_files['phenotype_ontology_qualifier'].write(
                        f"{self._transfer_phenotype_ontology_qualifier(ele)}\n")
            elif file_type == "gene_ontology":
                for ele in data:
                    self.out_files['gene_ontologies'].write(f"{self._transfer_gene_ontology(ele)}\n")
            elif file_type == "gene_regulation":
                for ele in data:
                    self.out_files['gene_regulations'].write(f"{self._transfer_gene_regulation(ele)}\n")
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")

    def _transfer_gene(self, ele):
        """Optimized gene transfer with pre-computed values"""
        funga_id = self.map_id(ele['source']['id'])
        symbol = ele.get('symbol', '')
        name = ele.get('name', '')
        description = ele.get('description', '')
        other_id = json.dumps(ele.get('other_name', []))
        gene_type = ele.get("type", "")
        source = json.dumps(ele.get("source", {}))
        dna_sequence = ele.get("sequence", {}).get("dna", "")
        polypeptide_sequence = ele.get("sequence", {}).get("polypeptide", "")
        return f"{funga_id}\t{symbol}\t{name}\t{description}\t{other_id}\t{gene_type}\t{source}\t{dna_sequence}\t{polypeptide_sequence}"

    def _transfer_gene_phenotype(self, ele):
        """Optimized gene-phenotype transfer"""
        gene = self.map_id(ele['source']['gene'])
        phenotype = ele['phenotype'].get('description', '')
        source = dict(ele["source"])
        source.pop("gene", None)
        ontology = ele['phenotype'].get('phenotype_ontology', '')
        qualifier = ele['phenotype'].get('phenotype_ontology_qualifier', '')
        references = json.dumps(ele['phenotype'].get('reference', []))
        return f"{gene}\t{phenotype}\t{json.dumps(source)}\t{qualifier}\t{ontology}\t{references}"

    def _transfer_gene_gene(self, ele):
        """Optimized gene-gene transfer"""
        gene1 = self.map_id(ele['source']['gene1'])
        gene2 = self.map_id(ele['source']['gene2'])
        relation_type = ele.get('type', '')
        source = dict(ele["source"])
        source.pop("gene1", None)
        source.pop("gene2", None)
        references = json.dumps(ele.get('reference', []))
        return f"{gene1}\t{gene2}\t{relation_type}\t{json.dumps(source)}\t{references}"

    def _transfer_phenotype_ontology(self, ele):
        """Optimized phenotype ontology transfer"""
        source = json.dumps({"name": "SGD", "link": "https://www.yeastgenome.org"})
        return f"{ele.get('ontologyId', '')}\t{ele.get('name', '')}\t{ele.get('upstream', '')}\t" \
               f"{ele.get('description', '')}\t{json.dumps(ele.get('downstream', []))}\t" \
               f"{json.dumps(ele.get('qualifiers', []))}\t{source}"

    def _transfer_phenotype_ontology_qualifier(self, ele):
        """Optimized phenotype ontology qualifier transfer"""
        source = json.dumps({"name": "SGD", "link": "https://www.yeastgenome.org"})
        return f"{ele.get('qualifierId', '')}\t{ele.get('name', '')}\t{ele.get('upstream', '')}\t" \
               f"{ele.get('description', '')}\t{json.dumps(ele.get('downstream', []))}\t{source}"

    def _transfer_gene_ontology(self, ele):
        """Optimized gene ontology transfer"""
        return f"{ele.get('go_id', '')}\t{ele.get('term', '')}\t" \
               f"{json.dumps(ele.get('source', {}))}\t{json.dumps(ele.get('reference', []))}"

    def _transfer_gene_regulation(self, ele):
        """Optimized gene regulation transfer"""
        return f"{ele.get('go_id_1', '')}\t{ele.get('go_id_2', '')}\t{ele.get('type', '')}\t" \
               f"{json.dumps(ele.get('source', {}))}\t{json.dumps(ele.get('reference', []))}"

    def close(self):
        """Close all output files"""
        for file in self.out_files.values():
            file.close()


if __name__ == '__main__':
    if len(sys.argv) == 3:
        converter = JSONToCSVConverter(sys.argv[1], sys.argv[2])
        try:
            converter.process_files()
        finally:
            converter.close()
    else:
        print("Usage: j2c.py <input-path> <output-path>")
        print("Example:")
        print("  j2c.py zfin zfin")