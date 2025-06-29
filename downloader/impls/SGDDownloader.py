import json
import os
from threading import Thread

import requests

from downloader.Downloader import Downloader

base_url = "https://www.yeastgenome.org/backend/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
class SGDDownloader(Downloader):
    fail_id = []
    download_cache_gene = []
    download_cache_gene_gene = []
    download_cache_gene_phenotype = []
    ids = []
    def markZero(self):
        self.download_cache_gene = []
        self.download_cache_gene_gene = []
        self.download_cache_gene_phenotype = []


    def start_gene(self):
        for id in self.ids:
            api_url = base_url + "locus/" + id.replace("\n", "")
            try:
                response = requests.get(api_url,headers=headers).json()
                if len(response) < 1:
                    response = requests.get(api_url,headers=headers).json()
                self.prepare_gene(response)
                print("成功:" + api_url)
            except Exception as e:
                self.fail_id.append(id + " gene")
                print("失败:" + api_url)
                print(e)
        if len(self.download_cache_gene) > 0:
            self.generateFile("gene", json.dumps(self.download_cache_gene))
        with open(self.name + "/fail.json",'a') as f:
            f.write(json.dumps(self.fail_id))

    def start_gene_phenotype(self):
        for id in self.ids:
            api_url = base_url + "locus/" + id.replace("\n", "") + "/phenotype_details"
            try:
                response = requests.get(api_url,headers=headers).json()
                if len(response) < 1:
                    response = requests.get(api_url,headers=headers).json()
                self.prepare_gene_phenotype(response)
                print("成功:" + api_url)
            except Exception as e:
                self.fail_id.append(id + " gene-phenotype")
                print("失败:" + api_url)
                print(e)
        if len(self.download_cache_gene_phenotype) > 0:
            self.generateFile("gene-phenotype", json.dumps(self.download_cache_gene_phenotype))
        with open(self.name + "/fail.json",'a') as f:
            f.write(json.dumps(self.fail_id))

    def start_gene_gene(self):
        for id in self.ids:
            api_url = base_url + "locus/" + id.replace("\n", "") + "/interaction_details"
            try:
                response = requests.get(api_url,headers=headers).json()
                if len(response) < 1:
                    response = requests.get(api_url,headers=headers).json()
                self.prepare_gene_gene(response)
                print("成功:" + api_url)
            except Exception as e:
                self.fail_id.append(id + " gene-gene")
                print("失败:" + api_url)
                print(e)
        if len(self.download_cache_gene_gene) > 0:
            self.generateFile("gene-gene", json.dumps(self.download_cache_gene_gene))
        with open(self.name + "/fail.json",'a') as f:
            f.write(json.dumps(self.fail_id))


    def download(self,args):
        self.create_dirs()
        self.markZero()
        with open(args[0], "r") as f:
            for id in f:
                self.ids.append(id)
        Thread(target=self.start_gene).start()
        Thread(target=self.start_gene_gene).start()
        Thread(target=self.start_gene_phenotype).start()

    def mapOntologyId(self,name):
        a = json.loads(open("SGD1/phenotype-ontology.json",'r').read())
        for o in a["datas"]:
            if o["name"] == name:
                return o["ontologyId"]
        return ""
    def mapQualifierIdId(self,name):
        a = json.loads(open("SGD1/phenotype-ontology-qualifier.json",'r').read())
        for o in a["datas"]:
            if o["name"] == name:
                return o["qualifierId"]
        return ""
    def create_dirs(self):
        os.makedirs(self.name + "/gene")
        os.makedirs(self.name + "/gene-gene")
        os.makedirs(self.name + "/gene-phenotype")

    def prepare_gene_phenotype(self,response):
        if response is None:
            return
        for phe in response:
            if len(self.download_cache_gene_phenotype) >= 1000:
                self.generateFile("gene-phenotype", json.dumps(self.download_cache_gene_phenotype))
                self.download_cache_gene_phenotype = []
            cache = {}
            cache["source"] = {
                "name": self.name,
                "link": phe["phenotype"]["link"],
                "gene": phe["locus"]["link"].split("/")[-1],
            }
            cache["extra"] = {}
            reference = []
            if phe["reference"]["pubmed_id"] is not None:
                reference.append("https://pubmed.ncbi.nlm.nih.gov/" + str(phe["reference"]["pubmed_id"]))

            if phe["experiment"]["link"]:
                reference.append("https://www.yeastgenome.org/"+phe["experiment"]["link"])
            cache["phenotype"] = {
                "description": phe["phenotype"]["display_name"],
                "reference":reference,
                "phenotype_ontology": self.mapOntologyId(str(phe["phenotype"]["display_name"].split(":")[0]).strip()),
            }
            try:
                cache["phenotype"]["phenotype_ontology_qualifier"] = self.mapQualifierIdId(
                    phe["phenotype"]["display_name"].split(":")[1].strip())
            except:
                cache["phenotype"]["phenotype_ontology_qualifier"] = []
            self.download_cache_gene_phenotype.append(cache)

    def prepare_gene_gene(self,response):
        if response is None:
            return
        for interact in response:
            if len(self.download_cache_gene_gene) >= 5000:
                self.generateFile("gene-gene", json.dumps(self.download_cache_gene_gene))
                self.download_cache_gene_gene = []
            cache = {}
            cache["type"] = interact["interaction_type"]
            cache["source"] = {
                "name": interact["source"]["display_name"] + " | SGD1",
                "link": "https://www.yeastgenome.org/locus/" +interact["locus1"]["link"].split("/")[-1] + "/interaction",
                "gene1":interact["locus1"]["link"].split("/")[-1],
                "gene2": interact["locus2"]["link"].split("/")[-1],
            }
            reference = ["https://pubmed.ncbi.nlm.nih.gov/"+str(interact["reference"]["pubmed_id"])]
            cache["reference"] = reference
            cache["extra"] = {}
            self.download_cache_gene_gene.append(cache)


    def grab_sequence(self,id):
        try:
            api_url = base_url + "locus/" + id + "/sequence_details"
            response = requests.get(api_url).json()
            dna = None
            polypeptide = None
            if "protein" in response:
                if len(response["protein"]) != 0:
                    polypeptide = response["protein"][0]["residues"]
            if "genomic_dna" in response:
                if len(response["genomic_dna"]) != 0:
                    dna = response["genomic_dna"][0]["residues"]

            return {
                "dna": dna,
                "polypeptide": polypeptide
            }
        except Exception as e:
            return {"dna": None,
                "polypeptide": None}

    def prepare_gene(self,response:dict):
        if response is None:
            return
        if len(self.download_cache_gene) >= 1000:
            self.generateFile("gene",json.dumps(self.download_cache_gene))
            self.download_cache_gene = []
        cache = {}
        cache["symbol"] = response["gene_name"]
        cache["name"] = response["name_description"]
        cache["description"] = response["description"]
        aliases = []
        for alia in response["aliases"]:
            if alia["category"] == "Alias":
                aliases.append(alia["display_name"])
        aliases.append(response["format_name"])
        cache["other_name"] = aliases
        cache["type"] = response["locus_type"]
        cache["source"] = {
            "name": self.name,
            "link":f"{base_url}locus/{response['sgdid']}",
            "id":response['sgdid']
        }
        cache["sequence"] = self.grab_sequence(response['sgdid'])
        cache["extra"] = {}
        self.download_cache_gene.append(cache)