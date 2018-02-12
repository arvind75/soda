from rpython.rlib.streamio import open_file_as_stream
from soda.lexer import lexer
import os

class Fetcher(object):
    def __init__(self):
        self.packages = []

    def add_package(self, package):
        self.packages.append(package)

    def fetch_tokens(self, data):
        tokenstream = lexer.lex(data)
        tokenlist = []
        fetch_found = False
        for token in tokenstream:
            tokenlist.append(token)

        for i in range(0, len(tokenlist)):
            if not fetch_found:
                if tokenlist[i].gettokentype() == "FETCH":
                    if not i == 0:
                        raise Exception("fetch error: fetch must precede main program")
                    else:
                        fetch_found = True
                else:
                    yield(tokenlist[i])
            else:
                if tokenlist[i].gettokentype() == "STRING":
                    p = tokenlist[i].getstr().strip("\"")
                    if p not in self.packages:
                        self.packages.append(p)
                else:
                    fetch_found = False
                    yield(tokenlist[i])

    def find(self):
        for package in self.packages:
            filepath = os.getcwd() + "/" + package + ".na"
            data = []
            tokenlist = []
            try:
                file = open_file_as_stream(filepath)
                data.append(file.readall())
                file.close()
                tokens = self.fetch_tokens("".join(data))
                tokenlist.append(tokens)
            except OSError:
                raise Exception("fetch error: package %s not found" % package)

            for tokens in tokenlist:
                for token in tokens:
                    yield token


fetcher = Fetcher()
