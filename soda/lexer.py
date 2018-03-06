from rply.token import Token, BaseBox, SourcePosition
from soda.errors import sodaError

whitespace = " \n\r\v\t"
newlines = "\n\r\v"
symbols = "!=<>&|()+-*/%^\"#"
alpha = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
numeric = "0123456789"
insertend = ["number", "string", ")"]
reserved = ["put", "fetch"]


class Lexer(BaseBox):
    def __init__(self):
        self.packages = []
        self.lasttoken = ""
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
            k = 0
            if source[i] == " " or source[i] == "\t":
                self.colno += 1
                i += 1
                continue
            elif source[i] == "\n":
                if self.lasttoken in insertend:
                    self.lasttoken = "END"
                    yield Token(name="END", value="END",
                                source_pos=SourcePosition(idx=self.idx,
                                                          lineno=self.lineno,
                                                          colno=self.colno))
                self.colno = 1
                self.lineno += 1
                i += 1
                continue
            elif source[i] == "\r" and source[i + 1] == "\n":
                if self.lasttoken in insertend:
                    self.lasttoken = "END"
                    yield Token(name="END", value="END",
                                source_pos=SourcePosition(idx=self.idx,
                                                          lineno=self.lineno,
                                                          colno=self.colno))
                self.colno = 1
                self.lineno += 1
                i += 2
                continue
            elif source[i] in symbols:
                if source[i] == "(":
                    self.lasttoken = "("
                    yield Token(name="(", value="(",
                                source_pos=SourcePosition(idx=self.idx,
                                                          lineno=self.lineno,
                                                          colno=self.colno))
                    self.colno += 1
                    i += 1
                    continue
                elif source[i] == ")":
                    self.lasttoken = ")"
                    yield Token(name=")", value=")",
                                source_pos=SourcePosition(idx=self.idx,
                                                          lineno=self.lineno,
                                                          colno=self.colno))
                    self.colno += 1
                    i += 1
                    continue
                elif source[i] == "+":
                    try:
                        if not (source[i + 1] in whitespace and source[i - 1]
                           in whitespace):
                            msg = (
                                "binary operator and its operands must " +
                                "be separated by whitespace")
                            self.lasttoken = "error"
                            yield Token(name="ERROR", value=msg,
                                        source_pos=SourcePosition(
                                            idx=self.idx,
                                            lineno=self.lineno,
                                            colno=self.colno))
                            break
                    except IndexError:
                        msg = (
                            "binary operator and its operands must "
                            "be separated by whitespace")
                        self.lasttoken = "error"
                        yield Token(name="ERROR", value=msg,
                                    source_pos=SourcePosition(
                                        idx=self.idx,
                                        lineno=self.lineno,
                                        colno=self.colno))
                        break
                    self.lasttoken = "+"
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
                        self.lasttoken = "number"
                        yield Token(name="NUMBER", value="".join(value),
                                    source_pos=SourcePosition(
                                        idx=self.idx,
                                        lineno=self.lineno,
                                        colno=self.colno))
                        self.colno += k
                        value = []
                        continue
                    try:
                        if not (source[i + 1] in whitespace and source[i - 1]
                           in whitespace):
                            msg = (
                                "binary operator and its operands must " +
                                "be separated by whitespace")
                            self.lasttoken = "error"
                            yield Token(name="ERROR", value=msg,
                                        source_pos=SourcePosition(
                                            idx=self.idx,
                                            lineno=self.lineno,
                                            colno=self.colno))
                            break
                    except IndexError:
                        msg = (
                            "binary operator and its operands must "
                            "be separated by whitespace")
                        self.lasttoken = "error"
                        yield Token(name="ERROR", value=msg,
                                    source_pos=SourcePosition(
                                        idx=self.idx,
                                        lineno=self.lineno,
                                        colno=self.colno))
                        break
                    self.lasttoken = "-"
                    yield Token(name="-", value="-",
                                source_pos=SourcePosition(idx=self.idx,
                                                          lineno=self.lineno,
                                                          colno=self.colno))
                    self.colno += 1
                    i += 1
                    continue
                elif source[i] == "*":
                    try:
                        if not (source[i + 1] in whitespace and source[i - 1]
                           in whitespace):
                            msg = (
                                "operator and its operands must "
                                "be separated by whitespace")
                            self.lasttoken = "error"
                            yield Token(name="ERROR", value=msg,
                                        source_pos=SourcePosition(
                                            idx=self.idx,
                                            lineno=self.lineno,
                                            colno=self.colno))
                            break
                    except IndexError:
                        msg = (
                            "binary operator and its operands must "
                            "be separated by whitespace")
                        self.lasttoken = "error"
                        yield Token(name="ERROR", value=msg,
                                    source_pos=SourcePosition(
                                        idx=self.idx,
                                        lineno=self.lineno,
                                        colno=self.colno))
                        break
                    self.lasttoken = "*"
                    yield Token(name="*", value="*",
                                source_pos=SourcePosition(idx=self.idx,
                                                          lineno=self.lineno,
                                                          colno=self.colno))
                    self.colno += 1
                    i += 1
                    continue
                elif source[i] == "/":
                    try:
                        if not (source[i + 1] in whitespace and source[i - 1]
                           in whitespace):
                            msg = (
                                "binary operator and its operands must " +
                                "be separated by whitespace")
                            self.lasttoken = "error"
                            yield Token(name="ERROR", value=msg,
                                        source_pos=SourcePosition(
                                            idx=self.idx,
                                            lineno=self.lineno,
                                            colno=self.colno))
                            break
                    except IndexError:
                        msg = (
                            "binary operator and its operands must "
                            "be separated by whitespace")
                        self.lasttoken = "error"
                        yield Token(name="ERROR", value=msg,
                                    source_pos=SourcePosition(
                                        idx=self.idx,
                                        lineno=self.lineno,
                                        colno=self.colno))
                        break
                    self.lasttoken = "/"
                    yield Token(name="/", value="/",
                                source_pos=SourcePosition(idx=self.idx,
                                                          lineno=self.lineno,
                                                          colno=self.colno))
                    self.colno += 1
                    i += 1
                    continue
                elif source[i] == "%":
                    try:
                        if not (source[i + 1] in whitespace and source[i - 1]
                           in whitespace):
                            msg = (
                                "binary operator and its operands must " +
                                "be separated by whitespace")
                            self.lasttoken = "error"
                            yield Token(name="ERROR", value=msg,
                                        source_pos=SourcePosition(
                                            idx=self.idx,
                                            lineno=self.lineno,
                                            colno=self.colno))
                            break
                    except IndexError:
                        msg = (
                            "binary operator and its operands must "
                            "be separated by whitespace")
                        self.lasttoken = "error"
                        yield Token(name="ERROR", value=msg,
                                    source_pos=SourcePosition(
                                        idx=self.idx,
                                        lineno=self.lineno,
                                        colno=self.colno))
                        break
                    self.lasttoken = "%"
                    yield Token(name="%", value="%",
                                source_pos=SourcePosition(idx=self.idx,
                                                          lineno=self.lineno,
                                                          colno=self.colno))
                    self.colno += 1
                    i += 1
                    continue
                elif source[i] == "^":
                    try:
                        if not (source[i + 1] in whitespace and source[i - 1]
                           in whitespace):
                            msg = (
                                "binary operator and its operands must " +
                                "be separated by whitespace")
                            self.lasttoken = "error"
                            yield Token(name="ERROR", value=msg,
                                        source_pos=SourcePosition(
                                            idx=self.idx,
                                            lineno=self.lineno,
                                            colno=self.colno))
                            break
                    except IndexError:
                        msg = (
                            "binary operator and its operands must "
                            "be separated by whitespace")
                        self.lasttoken = "error"
                        yield Token(name="ERROR", value=msg,
                                    source_pos=SourcePosition(
                                        idx=self.idx,
                                        lineno=self.lineno,
                                        colno=self.colno))
                        break
                    self.lasttoken = "^"
                    yield Token(name="^", value="^",
                                source_pos=SourcePosition(idx=self.idx,
                                                          lineno=self.lineno,
                                                          colno=self.colno))
                    self.colno += 1
                    i += 1
                    continue
                elif source[i] == "=":
                    try:
                        if source[i + 1] == "=":
                            if not (source[i + 2] in whitespace and
                                    source[i - 1] in whitespace):
                                msg = (
                                    "binary operator and its operands must " +
                                    "be separated by whitespace")
                                self.lasttoken = "error"
                                yield Token(name="ERROR", value=msg,
                                            source_pos=SourcePosition(
                                                idx=self.idx,
                                                lineno=self.lineno,
                                                colno=self.colno))
                                break
                            yield Token(name="==", value="==",
                                        source_pos=SourcePosition(
                                            idx=self.idx,
                                            lineno=self.lineno,
                                            colno=self.colno))
                            self.colno += 2
                            i += 2
                            continue
                        else:
                            if not (source[i + 1] in whitespace and
                                    source[i - 1] in whitespace):
                                msg = (
                                    "binary operator and its operands must " +
                                    "be separated by whitespace")
                                self.lasttoken = "error"
                                yield Token(name="ERROR", value=msg,
                                            source_pos=SourcePosition(
                                                idx=self.idx,
                                                lineno=self.lineno,
                                                colno=self.colno))
                                break
                            yield Token(name="=", value="=",
                                        source_pos=SourcePosition(
                                            idx=self.idx,
                                            lineno=self.lineno,
                                            colno=self.colno))
                            self.colno += 1
                            i += 1
                            continue
                    except IndexError:
                        msg = (
                            "binary operator and its operands must "
                            "be separated by whitespace")
                        self.lasttoken = "error"
                        yield Token(name="ERROR", value=msg,
                                    source_pos=SourcePosition(
                                        idx=self.idx,
                                        lineno=self.lineno,
                                        colno=self.colno))
                        break
                elif source[i] == "!":
                    try:
                        if source[i + 1] == "=":
                            if not (source[i + 2] in whitespace and
                                    source[i - 1] in whitespace):
                                msg = (
                                    "binary operator and its operands must " +
                                    "be separated by whitespace")
                                self.lasttoken = "error"
                                yield Token(name="ERROR", value=msg,
                                            source_pos=SourcePosition(
                                                idx=self.idx,
                                                lineno=self.lineno,
                                                colno=self.colno))
                                break
                            yield Token(name="!=", value="!=",
                                        source_pos=SourcePosition(
                                            idx=self.idx,
                                            lineno=self.lineno,
                                            colno=self.colno))
                            self.colno += 2
                            i += 2
                            continue
                        else:
                            msg = "unrecognized token %s" % source[i]
                            self.lasttoken = "error"
                            yield Token(name="ERROR",
                                        value=msg,
                                        source_pos=SourcePosition(
                                            idx=self.idx,
                                            lineno=self.lineno,
                                            colno=self.colno))
                            break
                    except IndexError:
                        msg = (
                            "binary operator and its operands must "
                            "be separated by whitespace")
                        self.lasttoken = "error"
                        yield Token(name="ERROR", value=msg,
                                    source_pos=SourcePosition(
                                        idx=self.idx,
                                        lineno=self.lineno,
                                        colno=self.colno))
                        break
                elif source[i] == "<":
                    try:
                        if source[i + 1] == "=":
                            if not (source[i + 2] in whitespace and
                                    source[i - 1] in whitespace):
                                msg = (
                                    "binary operator and its operands must " +
                                    "be separated by whitespace")
                                self.lasttoken = "error"
                                yield Token(name="ERROR", value=msg,
                                            source_pos=SourcePosition(
                                                idx=self.idx,
                                                lineno=self.lineno,
                                                colno=self.colno))
                                break
                            yield Token(name="<=", value="<=",
                                        source_pos=SourcePosition(
                                            idx=self.idx,
                                            lineno=self.lineno,
                                            colno=self.colno))
                            self.colno += 2
                            i += 2
                            continue
                        else:
                            if not (source[i + 1] in whitespace and
                                    source[i - 1] in whitespace):
                                msg = (
                                    "binary operator and its operands must " +
                                    "be separated by whitespace")
                                self.lasttoken = "error"
                                yield Token(name="ERROR", value=msg,
                                            source_pos=SourcePosition(
                                                idx=self.idx,
                                                lineno=self.lineno,
                                                colno=self.colno))
                                break
                            yield Token(name="<", value="<",
                                        source_pos=SourcePosition(
                                            idx=self.idx,
                                            lineno=self.lineno,
                                            colno=self.colno))
                            self.colno += 1
                            i += 1
                            continue
                    except IndexError:
                        msg = (
                            "binary operator and its operands must "
                            "be separated by whitespace")
                        self.lasttoken = "error"
                        yield Token(name="ERROR", value=msg,
                                    source_pos=SourcePosition(
                                        idx=self.idx,
                                        lineno=self.lineno,
                                        colno=self.colno))
                        break
                elif source[i] == ">":
                    try:
                        if source[i + 1] == "=":
                            if not (source[i + 2] in whitespace and
                                    source[i - 1] in whitespace):
                                msg = (
                                    "binary operator and its operands must " +
                                    "be separated by whitespace")
                                self.lasttoken = "error"
                                yield Token(name="ERROR", value=msg,
                                            source_pos=SourcePosition(
                                                idx=self.idx,
                                                lineno=self.lineno,
                                                colno=self.colno))
                                break
                            yield Token(name=">=", value=">=",
                                        source_pos=SourcePosition(
                                            idx=self.idx,
                                            lineno=self.lineno,
                                            colno=self.colno))
                            self.colno += 2
                            i += 2
                            continue
                        else:
                            if not (source[i + 1] in whitespace and
                                    source[i - 1] in whitespace):
                                msg = (
                                    "binary operator and its operands must " +
                                    "be separated by whitespace")
                                self.lasttoken = "error"
                                yield Token(name="ERROR", value=msg,
                                            source_pos=SourcePosition(
                                                idx=self.idx,
                                                lineno=self.lineno,
                                                colno=self.colno))
                                break
                            yield Token(name=">", value=">",
                                        source_pos=SourcePosition(
                                            idx=self.idx,
                                            lineno=self.lineno,
                                            colno=self.colno))
                            self.colno += 1
                            i += 1
                            continue
                    except IndexError:
                        msg = (
                            "binary operator and its operands must "
                            "be separated by whitespace")
                        self.lasttoken = "error"
                        yield Token(name="ERROR", value=msg,
                                    source_pos=SourcePosition(
                                        idx=self.idx,
                                        lineno=self.lineno,
                                        colno=self.colno))
                        break
                elif source[i] == "&":
                    try:
                        if not (source[i + 1] in whitespace and source[i - 1]
                           in whitespace):
                            msg = (
                                "binary operator and its operands must " +
                                "be separated by whitespace")
                            self.lasttoken = "error"
                            yield Token(name="ERROR", value=msg,
                                        source_pos=SourcePosition(
                                            idx=self.idx,
                                            lineno=self.lineno,
                                            colno=self.colno))
                            break
                    except IndexError:
                        msg = (
                            "binary operator and its operands must "
                            "be separated by whitespace")
                        self.lasttoken = "error"
                        yield Token(name="ERROR", value=msg,
                                    source_pos=SourcePosition(
                                        idx=self.idx,
                                        lineno=self.lineno,
                                        colno=self.colno))
                        break
                    self.lasttoken = "&"
                    yield Token(name="&", value="&",
                                source_pos=SourcePosition(idx=self.idx,
                                                          lineno=self.lineno,
                                                          colno=self.colno))
                    self.colno += 1
                    i += 1
                    continue
                elif source[i] == "|":
                    try:
                        if not (source[i + 1] in whitespace and source[i - 1]
                           in whitespace):
                            msg = (
                                "binary operator and its operands must " +
                                "be separated by whitespace")
                            self.lasttoken = "error"
                            yield Token(name="ERROR", value=msg,
                                        source_pos=SourcePosition(
                                            idx=self.idx,
                                            lineno=self.lineno,
                                            colno=self.colno))
                            break
                    except IndexError:
                        msg = (
                            "binary operator and its operands must "
                            "be separated by whitespace")
                        self.lasttoken = "error"
                        yield Token(name="ERROR", value=msg,
                                    source_pos=SourcePosition(
                                        idx=self.idx,
                                        lineno=self.lineno,
                                        colno=self.colno))
                        break
                    self.lasttoken = "|"
                    yield Token(name="|", value="|",
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
                        self.lasttoken = "error"
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
                            self.lasttoken = "error"
                            yield Token(name="ERROR",
                                        value=msg,
                                        source_pos=SourcePosition(
                                            idx=self.idx,
                                            lineno=self.lineno,
                                            colno=self.colno))
                            break
                        if source[j] in newlines:
                            msg = "newline in string"
                            self.lasttoken = "error"
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
                                k += 2
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
                                msg = ("unknown escape sequence \\%s"
                                       % source[j + 1])
                                self.lasttoken = "error"
                                yield Token(name="ERROR",
                                            value=msg,
                                            source_pos=SourcePosition(
                                                idx=self.idx,
                                                lineno=self.lineno,
                                                colno=self.colno))
                                j += 2
                                k += 2
                                continue
                        else:
                            value.append(source[j])
                            j += 1
                            k += 1
                    self.lasttoken = "string"
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
                self.lasttoken = "number"
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
                    if iden == "put":
                        self.lasttoken = "put"
                        yield Token(name="PUT", value=iden,
                                    source_pos=SourcePosition(
                                        idx=self.idx,
                                        lineno=self.lineno,
                                        colno=self.colno))
                    elif iden == "fetch":
                        self.lasttoken = "fetch"
                        yield Token(name="FETCH", value=iden,
                                    source_pos=SourcePosition(
                                        idx=self.idx,
                                        lineno=self.lineno,
                                        colno=self.colno))
                else:
                    # IDEN TOKEN HERE
                    sodaError("test", "-1", "-1", "iden not recognized")
                value = []
                i = j
                self.colno += k
            else:
                msg = "unrecognized token %s" % source[i]
                self.lasttoken = "error"
                yield Token(name="ERROR",
                            value=msg,
                            source_pos=SourcePosition(
                                idx=self.idx,
                                lineno=self.lineno,
                                colno=self.colno))
                break
        if self.lasttoken in insertend:
            self.lasttoken = "END"
            yield Token(name="END", value="END",
                        source_pos=SourcePosition(
                            idx=self.idx,
                            lineno=self.lineno,
                            colno=self.colno))


lexer = Lexer()
