from rply.token import Token, BaseBox, SourcePosition
import os

whitespace = " \n\r\v\t"
newlines = "\n\r\v"
symbols = "()+-*/%^\"#"
alpha = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
numeric = "123456789"
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
                    self.colno += 1
                    yield Token(name="(", value="(",
                                source_pos=SourcePosition(idx=self.idx,
                                                          lineno=self.lineno,
                                                          colno=self.colno))
                    i += 1
                    continue
                elif source[i] == ")":
                    
                    self.colno += 1
                    yield Token(name=")", value=")",
                                source_pos=SourcePosition(idx=self.idx,
                                                          lineno=self.lineno,
                                                          colno=self.colno))
                    i += 1
                    continue
                elif source[i] == "+":
                    
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
                        
                        i = j
                        yield Token(name="NUMBER", value="".join(value),
                                    source_pos=SourcePosition(idx=self.idx,
                                                              lineno=self.lineno,
                                                              colno=self.colno))
                        value = []
                        continue
                    
                    self.colno += 1
                    yield Token(name="-", value="-",
                                source_pos=SourcePosition(idx=self.idx,
                                                          lineno=self.lineno,
                                                          colno=self.colno))
                    i += 1
                    continue
                elif source[i] == "*":
                    
                    self.colno += 1
                    yield Token(name="*", value="*",
                                source_pos=SourcePosition(idx=self.idx,
                                                          lineno=self.lineno,
                                                          colno=self.colno))
                    i += 1
                    continue
                elif source[i] == "/":
                    
                    self.colno += 1
                    yield Token(name="/", value="/",
                                source_pos=SourcePosition(idx=self.idx,
                                                          lineno=self.lineno,
                                                          colno=self.colno))
                    i += 1
                    continue
                elif source[i] == "%":
                    
                    self.colno += 1
                    yield Token(name="%", value="%",
                                source_pos=SourcePosition(idx=self.idx,
                                                          lineno=self.lineno,
                                                          colno=self.colno))
                    i += 1
                    continue
                elif source[i] == "^":
                    
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
                        msg = "string not terminated"
                        yield Token(name="ERROR",
                                    value=msg,
                                    source_pos=SourcePosition(
                                        idx=self.idx,
                                        lineno=self.lineno,
                                        colno=self.colno))
                        break
                    self.colno += 1
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
                            self.colno += 1
                            j += 1
                    
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
