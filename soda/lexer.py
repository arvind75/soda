from rply.token import Token, BaseBox, SourcePosition
import os

whitespace = " \n\r\v\t"
newlines = "\n\r\v"
symbols = "()+-*/%^\"#"
alpha = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
numeric = "0123456789"
reserved = ["Println", "fetch"]

class Lexer(BaseBox):
    def __init__(self):
        self.packages = []
        self.idx = 0
        self.lineno = 1
        self.colno = 1

    def lex(self, source, idx):
        self.lineno = 1
        self.colno = 1
        self.idx = idx
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
                    yield Token(name="(", value="(",
                                source_pos=SourcePosition(idx=self.idx,
                                                          lineno=self.lineno,
                                                          colno=self.colno))
                    self.colno += 1
                    i += 1
                    continue
                elif source[i] == ")":                    
                    yield Token(name=")", value=")",
                                source_pos=SourcePosition(idx=self.idx,
                                                          lineno=self.lineno,
                                                          colno=self.colno))
                    self.colno += 1
                    i += 1
                    continue
                elif source[i] == "+":
                    yield Token(name="+", value="+",
                                source_pos=SourcePosition(idx=self.idx,
                                                          lineno=self.lineno,
                                                          colno=self.colno))
                    self.colno += 1
                    i += 1
                    continue
                elif source[i] == "-":
                    if source[i + 1] in numeric:
                        k = 0
                        value.append("-")
                        j = i + 1
                        while source[j] in numeric:
                            value.append(source[j])
                            k += 1
                            j += 1
                            try:
                                source[j]
                            except IndexError:
                                break
                        
                        i = j
                        yield Token(name="NUMBER", value="".join(value),
                                    source_pos=SourcePosition(idx=self.idx,
                                                              lineno=self.lineno,
                                                              colno=self.colno))
                        self.colno += k
                        value = []
                        continue
                    
                    yield Token(name="-", value="-",
                                source_pos=SourcePosition(idx=self.idx,
                                                          lineno=self.lineno,
                                                          colno=self.colno))
                    self.colno += 1
                    i += 1
                    continue
                elif source[i] == "*": 
                    yield Token(name="*", value="*",
                                source_pos=SourcePosition(idx=self.idx,
                                                          lineno=self.lineno,
                                                          colno=self.colno))
                    self.colno += 1
                    i += 1
                    continue
                elif source[i] == "/":
                    yield Token(name="/", value="/",
                                source_pos=SourcePosition(idx=self.idx,
                                                          lineno=self.lineno,
                                                          colno=self.colno))
                    self.colno += 1
                    i += 1
                    continue
                elif source[i] == "%":
                    yield Token(name="%", value="%",
                                source_pos=SourcePosition(idx=self.idx,
                                                          lineno=self.lineno,
                                                          colno=self.colno))
                    self.colno += 1
                    i += 1
                    continue
                elif source[i] == "^":
                    yield Token(name="^", value="^",
                                source_pos=SourcePosition(idx=self.idx,
                                                          lineno=self.lineno,
                                                          colno=self.colno))
                    self.colno += 1
                    i += 1
                    continue
                elif source[i] == "\"":
                    k = 0
                    j = i + 1
                    try:
                        source[j]
                    except IndexError:
                        msg = "string not terminated"
                        yield Token(name="ERROR",
                                    value=msg,
                                    source_pos=SourcePosition(
                                        idx=self.idx,
                                        lineno=self.lineno,
                                        colno=self.colno))
                        break
                    while not source[j] == "\"":
                        try:
                            source[j + 1]
                        except IndexError:
                            msg = "string not terminated"
                            yield Token(name="ERROR",
                                        value=msg,
                                        source_pos=SourcePosition(
                                            idx=self.idx,
                                            lineno=self.lineno,
                                            colno=self.colno))
                            break
                        if source[j] in newlines:
                            msg = "newline in string"
                            yield Token(name="ERROR",
                                        value=msg,
                                        source_pos=SourcePosition(
                                            idx=self.idx,
                                            lineno=self.lineno,
                                            colno=self.colno))
                            break
                        elif source[j] == "\\":
                            if source[j + 1] == "\\":
                                value.append("\\")
                                j += 2
                                k += 2
                                continue
                            elif source[j + 1] == "n":
                                value.append("\n")
                                j += 2
                                K += 2
                                continue
                            elif source[j + 1] == "t":
                                value.append("\t")
                                j += 2
                                k += 2
                                continue
                            elif source[j + 1] == "r":
                                value.append("\r")
                                j += 2
                                k += 2
                                continue
                            elif source[j + 1] == "v":
                                value.append("\v")
                                j += 2
                                k += 2
                                continue
                            elif source[j + 1] == "\"":
                                value.append("\"")
                                j += 2
                                k += 2
                                continue
                            else:
                                msg = "unknown escape sequence \\%s" % source[j + 1]
                                yield Token(name="ERROR",
                                            value=msg,
                                            source_pos=SourcePosition(
                                                idx=self.idx,
                                                lineno=self.lineno,
                                                colno=self.colno))
                                break
                        else:
                            value.append(source[j])
                            j += 1
                            k += 1
                    yield Token(name="STRING", value="".join(value),
                                source_pos=SourcePosition(idx=self.idx,
                                                          lineno=self.lineno,
                                                          colno=self.colno))
                    value = []
                    i = j + 1
                    self.colno += k
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
                k = 0
                while source[j] in numeric:
                    value.append(source[j])
                    j += 1
                    k += 1
                    try:
                        source[j]
                    except IndexError:
                        break
                
                i = j
                yield Token(name="NUMBER", value="".join(value),
                            source_pos=SourcePosition(idx=self.idx,
                                                      lineno=self.lineno,
                                                      colno=self.colno))
                self.colno += k
                value = []
                continue
            elif source[i] in alpha:
                j = i
                k = 0
                while not source[j] in whitespace:
                    value.append(source[j])
                    j += 1
                    k += 1
                    try:
                        source[j]
                    except IndexError:
                        break
                iden = "".join(value)
                if iden in reserved:
                    if iden == "Println":
                        
                        yield Token(name="PRINTLN", value=iden,
                                    source_pos=SourcePosition(idx=self.idx,
                                                              lineno=self.lineno,
                                                              colno=self.colno))
                    elif iden == "fetch":
                        yield Token(name="FETCH", value=iden,
                                    source_pos=SourcePosition(idx=self.idx,
                                                              lineno=self.lineno,
                                                              colno=self.colno))       
                else:
                    pass # IDENTIFIER TOK HERE
                value = []
                i = j
                self.colno += k
            else:
                msg = "unrecognized token %s" % source[i]
                yield Token(name="ERROR",
                            value=msg,
                            source_pos=SourcePosition(
                                idx=self.idx,
                                lineno=self.lineno,
                                colno=self.colno))
                break
                
lexer = Lexer()
