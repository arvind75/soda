from rpython.rlib.streamio import open_file_as_stream
from soda.lexer import lexer
from soda.errors import sodaError
import soda.parser
import os

class Fetcher(object):
    def __init__(self):
        self.packages = []
        self.tokgeneratorlist = []

    def fetch(self):
        for package in self.packages:
            fetch_found = False
            filepath = os.getcwd() + "/" + package + ".na"
            try:
                sourcefile = open_file_as_stream(filepath)
                data = sourcefile.readall()
                sourcefile.close()
            except OSError:
                sodaError("package \"%s\" not found" % package)
            i = 0
            tokenlist = []
            for token in lexer.lex(data):
                if not fetch_found:
                    if token.name == "FETCH":
                        if not i == 0:
                            sodaError("fetch statement must precede main program")
                        else:
                            i += 1
                            fetch_found = True
                    else:
                        i += 1
                        tokenlist.append(token)
                else:
                    if token.name == "STRING":
                        if token.value not in self.packages:
                            self.packages.append(token.value)
                        elif token.value == self.packages[0]:
                            sodaError("cannot import root package \"%s\"" % token.value)
                    else:
                        tokenlist.append(token)
                        fetch_found = False
            self.tokgeneratorlist.append(tokenlist)

    def gettokens(self):
        self.fetch()
        self.packages.reverse()
        self.tokgeneratorlist.reverse()
        j = 0
        for generators in self.tokgeneratorlist:
            soda.parser.currentdir = self.packages[j]
            for token in generators:
                yield token
            j += 1
    
fetcher = Fetcher()
