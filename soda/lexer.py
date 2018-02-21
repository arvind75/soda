from rply.token import Token, BaseBox, SourcePosition

whitespace = " \n\r\v\t"
escapes = "\n\r\v\t"
symbols = "()+-*/%^\"#"
alpha = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
numeric = "0123456789"
reserved = ["Println", "fetch"]

class Lexer(BaseBox):
    def __init__(self, idx=-1, lineno=1, colno=1):
        self.idx = idx
        self.lineno = lineno
        self.colno = colno

    def lex(self, source, package): # function should emit a package token
                                    # to help parser manage state
        i = 0
        value = []
        while i < len(source):
            if source[i] == " " or source[i] == "\t":
                self.colno += 1
                i += 1
                continue
            elif source[i] == "\n":
                self.colno = 1
                self.lineno += 1
                i += 1
                continue
            elif source[i] == "\r" and source[i + 1] == "\n":
                self.colno = 1
                self.lineno += 1
                i += 2
                continue
            elif source[i] in symbols:
                if source[i] == "(":
                    self.idx += 1
                    self.colno += 1
                    yield Token(name="(", value="(",
                                source_pos=SourcePosition(idx=self.idx,
                                                          lineno=self.lineno,
                                                          colno=self.colno))
                    i += 1
                    continue
                elif source[i] == ")":
                    self.idx += 1
                    self.colno += 1
                    yield Token(name=")", value=")",
                                source_pos=SourcePosition(idx=self.idx,
                                                          lineno=self.lineno,
                                                          colno=self.colno))
                    i += 1
                    continue
                elif source[i] == "+":
                    self.idx += 1
                    self.colno += 1
                    yield Token(name="+", value="+",
                                source_pos=SourcePosition(idx=self.idx,
                                                          lineno=self.lineno,
                                                          colno=self.colno))
                    i += 1
                    continue
                elif source[i] == "-":
                    if source[i + 1] in numeric:
                        value.append("-")
                        j = i + 1
                        while source[j] in numeric:
                            value.append(source[j])
                            self.colno += 1
                            j += 1
                            try:
                                source[j]
                            except IndexError:
                                break
                        self.idx += 1
                        i = j
                        yield Token(name="NUMBER", value="".join(value),
                                    source_pos=SourcePosition(idx=self.idx,
                                                              lineno=self.lineno,
                                                              colno=self.colno))
                        value = []
                        continue
                    self.idx += 1
                    self.colno += 1
                    yield Token(name="-", value="-",
                                source_pos=SourcePosition(idx=self.idx,
                                                          lineno=self.lineno,
                                                          colno=self.colno))
                    i += 1
                    continue
                elif source[i] == "*":


                    self.idx += 1
                    self.colno += 1
                    yield Token(name="*", value="*",
                                source_pos=SourcePosition(idx=self.idx,
                                                          lineno=self.lineno,
                                                          colno=self.colno))
                    i += 1
                    continue
                elif source[i] == "/":


                    self.idx += 1
                    self.colno += 1
                    yield Token(name="/", value="/",
                                source_pos=SourcePosition(idx=self.idx,
                                                          lineno=self.lineno,
                                                          colno=self.colno))
                    i += 1
                    continue
                elif source[i] == "%":


                    self.idx += 1
                    self.colno += 1
                    yield Token(name="%", value="%",
                                source_pos=SourcePosition(idx=self.idx,
                                                          lineno=self.lineno,
                                                          colno=self.colno))
                    i += 1
                    continue
                elif source[i] == "^":


                    self.idx += 1
                    self.colno += 1
                    yield Token(name="^", value="^",
                                source_pos=SourcePosition(idx=self.idx,
                                                          lineno=self.lineno,
                                                          colno=self.colno))
                    i += 1
                    continue
                elif source[i] == "\"":
                    j = i + 1
                    try:
                        source[j]
                    except IndexError:
                        break # EMIT BAD STRING TOKEN HERE
                    self.colno += 1
                    while not source[j] == "\"":
                        try:
                            source[j + 1]
                        except IndexError:
                            break
                        if source[j] in escapes:
                            break
                        elif source[j] == "\\":
                            if source[j + 1] == "\\":
                                value.append("\\")
                                self.colno += 2
                                j += 2
                                continue
                            elif source[j + 1] == "n":
                                value.append("\n")
                                self.colno += 2
                                j += 2
                                continue
                            elif source[j + 1] == "t":
                                value.append("\t")
                                self.colno += 2
                                j += 2
                                continue
                            elif source[j + 1] == "r":
                                value.append("\r")
                                self.colno += 2
                                j += 2
                                continue
                            elif source[j + 1] == "v":
                                value.append("\v")
                                self.colno += 2
                                j += 2
                                continue
                            elif source[j + 1] == "\"":
                                value.append("\"")
                                self.colno += 2
                                j += 2
                                continue
                            else:
                                break # EMIT BAD ESCAPE TOKEN
                        else:
                            value.append(source[j])
                            self.colno += 1
                            j += 1
                    self.idx += 1
                    self.colno += 1
                    yield Token(name="STRING", value="".join(value),
                                source_pos=SourcePosition(idx=self.idx,
                                                          lineno=self.lineno,
                                                          colno=self.colno))
                    value = []
                    i = j + 1
                    continue
                elif source[i] == "#":
                    j = i
                    while not (source[j] == "\n" or source[j] == "\r"):
                        j += 1
                        try:
                            source[j]
                        except IndexError:
                            break
                    i = j
                    continue
            elif source[i] in numeric:
                j = i
                while source[j] in numeric:
                    value.append(source[j])
                    self.colno += 1
                    j += 1
                    try:
                        source[j]
                    except IndexError:
                        break
                self.idx += 1
                i = j
                yield Token(name="NUMBER", value="".join(value),
                            source_pos=SourcePosition(idx=self.idx,
                                                      lineno=self.lineno,
                                                      colno=self.colno))
                value = []
                continue
            elif source[i] in alpha:
                j = i
                while not source[j] in whitespace:
                    value.append(source[j])
                    self.colno += 1
                    j += 1
                    try:
                        source[j]
                    except IndexError:
                        break
                iden = "".join(value)
                if iden in reserved:
                    if iden == "Println":
                        self.idx += 1
                        yield Token(name="PRINTLN", value=iden,
                                    source_pos=SourcePosition(idx=self.idx,
                                                              lineno=self.lineno,
                                                              colno=self.colno))
                    elif iden == "fetch":
                        self.idx += 1
                        yield Token(name="FETCH", value=iden,
                                    source_pos=SourcePosition(idx=self.idx,
                                                              lineno=self.lineno,
                                                              colno=self.colno))
                else:
                    pass # IDENTIFIER TOK HERE
                value = []
                i = j       
            else:
                i += 1   # UNRECOGNIZED TOK HERE
                
lexer = Lexer()
