
class Downloader:
    def __init__(self,name):
        self.name = name
        self.index = 0
    def download(self,args:list):
        pass

    def generateFile(self,path:str,content:str):
        self.index += 1
        with open(self.name + f"/{path}/{self.index}.json",'w') as f:
            f.write(content)

downloaders = []

def get_downloader(name:str):
    for downloader in downloaders:
        if downloader.name == name:
            return downloader
    return None

