from rpython.rlib.streamio import open_file_as_stream
from soda.lexer import lexer
from soda.errors import sodaError


class Fetcher(object):
    def __init__(self):
        self.idx = 0
        self.data = ""
        self.recentpath = ""
        self.tokentopackage = {}
        self.packages = []
        self.tokgeneratorlist = []

    def addpackage(self, filepath):
        pathlist = filepath.split("/")
        package = pathlist.pop()
        if not pathlist == []:
            self.recentpath += "/".join(pathlist) + "/"
        self.packages.append(package)

    def fetch(self):
        for package in self.packages:
            fetch_found = False
            filepath = self.recentpath + package + ".na"
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
            if not self.data == "":
                for token in lexer.lex(self.data, self.idx):
                    if not fetch_found:
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
                                fetch_found = True
                        else:
                            i += 1
                            tokenlist.append(token)
                    else:
                        if token.name == "STRING":
                            pathlist = token.value.split("/")
                            pname = pathlist.pop()
                            if pname not in self.packages:
                                self.addpackage(token.value)
                                self.tokentopackage[pname] = token
                            elif pname == self.packages[0]:
                                sodaError(
                                    package,
                                    str(token.getsourcepos().lineno),
                                    str(token.getsourcepos().colno),
                                    "cannot import root package \"%s\""
                                    % pname
                                )
                        else:
                            tokenlist.append(token)
                            fetch_found = False
            self.idx += 1
            self.data = ""
            self.tokgeneratorlist.append(tokenlist)

    def gettokens(self):
        self.fetch()
        self.tokgeneratorlist.reverse()
        for generators in self.tokgeneratorlist:
            for token in generators:
                yield token


fetcher = Fetcher()
