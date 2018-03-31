from rpython.rlib.streamio import open_file_as_stream
from rpython.rlib.rpath import rnormpath
from soda.lexer import lexer
from soda.errors import sodaError


class Fetcher(object):
    def __init__(self):
        self.idx = 0
        self.pathtopackage = {}
        self.tokentopackage = {}
        self.fullpaths = []
        self.packages = []
        self.tokgeneratorlist = []

    def addpackage(self, filepath):
        normpath = rnormpath(filepath)
        dirlist = normpath.split("/")
        package = dirlist.pop()
        finalpath = "/".join(dirlist) + "/"
        if finalpath + package not in self.fullpaths:
            self.pathtopackage[package] = finalpath
            self.packages.append(package)
            self.fullpaths.append(finalpath + package)

    def fetch(self):
        data = ""
        for package in self.packages:
            fetchfound = False
            packagefound = False
            filepath = self.pathtopackage[package] + package + ".na"
            try:
                sourcefile = open_file_as_stream(filepath)
                data = sourcefile.readall()
                sourcefile.close()
            except OSError:
                errtok = self.tokentopackage.get(package, None)
                errfile = self.packages[errtok.getsourcepos().idx]
                sodaError(errfile, str(errtok.getsourcepos().lineno),
                          str(errtok.getsourcepos().colno),
                          "package \"%s\" not found" % package)
            i = 0
            tokenlist = []
            if not data == "":
                for token in lexer.lex(data, self.idx):
                    if not fetchfound:
                        if token.name == "FETCH":
                            if not i == 0:
                                sodaError(
                                    package,
                                    str(token.getsourcepos().lineno),
                                    str(token.getsourcepos().colno),
                                    "fetch statement must precede main program"
                                )
                            else:
                                i += 1
                                fetchfound = True
                        else:
                            i += 1
                            tokenlist.append(token)
                    else:
                        if token.name == "STRING":
                            self.tokentopackage[
                                token.value] = token
                            if not packagefound:
                                fullpath = self.pathtopackage[
                                    self.packages[self.idx]] + token.value
                                self.addpackage(fullpath)
                                packagefound = True
                                continue
                            else:
                                sodaError(
                                    package,
                                    str(token.getsourcepos().lineno),
                                    str(token.getsourcepos().colno),
                                    "package names must be "
                                    "separated by newlines"
                                )
                        elif token.name == "END":
                            packagefound = False
                            continue
                        else:
                            tokenlist.append(token)
                            fetchfound = False
            data = ""
            self.idx += 1
            self.tokgeneratorlist.append(tokenlist)

    def gettokens(self):
        self.fetch()
        self.tokgeneratorlist.reverse()
        for generators in self.tokgeneratorlist:
            for token in generators:
                yield token


fetcher = Fetcher()
