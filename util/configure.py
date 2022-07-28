import sys

from util.txtparser import TXTParser
import util

# file: "{yyyymmdd-number}.config"

class ConfigureManager:

    def __init__(self):

        super().__init__()
        try:
            self.url = util.findLatestFile("./db_files/config", ".config")
            print('Now config file:', self.url)
        except LookupError as e:
            print('Please add a config file')
            sys.exit()

        self.readFile()

    def readFile(self):

        self.parser = TXTParser(self.url)
        self.dict = self.parser.dict

        self.subjects = self.dict['subjects'] if ("subjects" in self.dict) else []

if __name__ == '__main__':
    cm = ConfigureManager()
    print(cm.subjects)









