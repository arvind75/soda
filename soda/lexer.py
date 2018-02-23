from rply.token import Token, BaseBox, SourcePosition
import os

whitespace = " \n\r\v\t"
newlines = "\n\r\v"
symbols = "()+-*/%^\"#"
alpha = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
numeric = "123456789"
numeric2 = "0123456789.eE-+"
reserved = ["Println", "fetch"]

class Lexer(BaseBox):
    def __init__(self, packages=[], idx=-1, lineno=1, colno=1):
        self.packages = packages
        self.idx = idx
        self.lineno = lineno
        self.colno = colno

    def lex(self, source):
        self.lineno = 1
        self.colno = 1
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
                        break # EMIT BAD STRING TOKEN HERE
                    self.colno += 1
                    while not source[j] == "\"":
                        try:
                            source[j + 1]
                        except IndexError:
                            break # BAD STRING
                        if source[j] in newlines:
                            break # BAD STRING - NEWLINE
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
                while source[j] in numeric2:
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
                i += 1   # UNRECOGNIZED TOK HERE
                
lexer = Lexer()
