from rpython.rlib.streamio import open_file_as_stream
from rply.errors import LexingError
from soda.lexer import lexer
from soda.errors import sodaError
import os

class Fetcher(object):
    def __init__(self):
        self.packages = []

    def add_package(self, package):
        self.packages.append(package)

    def fetch_tokens(self, data):
        tokenlist = []
        fetch_found = False
        try:
            for token in lexer.lex(data):
                tokenlist.append(token)
        except LexingError as LE:
            print("errored out, man!")
            os._exit(1)
            
        for i in range(0, len(tokenlist)):
            if not fetch_found:
                if tokenlist[i].gettokentype() == "FETCH":
                    if not i == 0:
                        sodaError("fetch statement must precede main program")
                        pass
                    else:
                        fetch_found = True
                else:
                    yield(tokenlist[i])
            else:
                if tokenlist[i].gettokentype() == "STRING":
                    p = tokenlist[i].getstr().strip("\"")
                    if p == self.packages[0]:
                        sodaError("cannot fetch root package \"%s\"" % p)
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
                sodaError("package \"%s\" not found" % package)

            for tokens in tokenlist:
                for token in tokens:
                    yield token


fetcher = Fetcher()
