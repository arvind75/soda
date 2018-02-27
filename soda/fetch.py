from rpython.rlib.streamio import open_file_as_stream
from soda.lexer import lexer
from soda.errors import sodaError
import os

class Fetcher(object):
    def __init__(self):
        self.data = ""
        self.tokentopackage = {}
        self.packages = []
        self.tokgeneratorlist = []

    def fetch(self):
        idx = 0
        for package in self.packages:
            fetch_found = False
            filepath = package + ".na"
            try:
                sourcefile = open_file_as_stream(filepath)
                self.data = sourcefile.readall()
                sourcefile.close()
            except OSError:
                errtok = self.tokentopackage.get(package, None)
                errfile = self.packages[errtok.getsourcepos().idx]
                sodaError(errfile, str(errtok.getsourcepos().lineno),
                          str(errtok.getsourcepos().colno),
                          "package \"%s\" not found" % package)
            i = 0
            tokenlist = []
            for token in lexer.lex(self.data, idx):
                if not fetch_found:
                    if token.name == "FETCH":
                        if not i == 0:
                            sodaError(package, str(token.getsourcepos().lineno),
                                      str(token.getsourcepos().colno),
                                      "fetch statement must precede main program")
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
                            self.tokentopackage[token.value] = token
                        elif token.value == self.packages[0]:
                            sodaError(package, str(token.getsourcepos().lineno),
                                      str(token.getsourcepos().colno),
                                      "cannot import root package \"%s\"" % token.value)
                    else:
                        tokenlist.append(token)
                        fetch_found = False
            idx += 1
            self.tokgeneratorlist.append(tokenlist)

    def gettokens(self):
        self.fetch()
        self.tokgeneratorlist.reverse()
        j = 0
        for generators in self.tokgeneratorlist:
            for token in generators:
                yield token
            j += 1
    
fetcher = Fetcher()
