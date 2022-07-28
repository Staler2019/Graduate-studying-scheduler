import re

# str.strip() 去除 [ \r\n\t]

class TXTParser:

    def __init__(self, file_loc):

        super().__init__()
        self.dict = {}
        self.url = file_loc
        self.parse()

    def parse(self):

        with open(self.url,'r',encoding='utf-8') as f:
            for line in f.readlines():
                line = line.strip()
                if line[0] == "#": # comment
                    continue
                else:
                    line = line.split("=")
                    for i in range(len(line)): # remove front, end's blanks
                        line[i] = line[i].strip()
                    if line[1][0] == "[": # array
                        line_backs = line[1][1:-1].split(',')

                        for i in range(len(line_backs)):
                            line_backs[i] = line_backs[i].strip()

                        self.dict[line[0]] = line_backs
                    else:
                        self.dict[line[0]] = line[1]

        def getDict(self):

            return self.dict()

