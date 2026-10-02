import json

class FileManager:
    """
    class for managing json files
    """
    def __init__(self):
        self.filePath = '../data/catalog.json'
        self.dictJFile = None
    
    def readJFile(self):
        self.dictJFile = json.load(open(self.filePath))

        print(self.dictJFile)

    def searchByName(self, name):
        pass


if __name__ == "__main__":

    sensorFile = FileManager()
    sensorFile.readJFile()