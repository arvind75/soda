from rply.token import Token, BaseBox, SourcePosition

whitespace = " \n\r\v\t"
newlines = "\n\r\v"
symbols = ":.,;!=<>&|()[]+-*/%^\"#"
numeric = "0123456789"
insertend = ["number", "string", "identifier",
             ")", "]", "break", "end"]
reserved = ["fetch", "func", "where", "if",
            "then", "else", "for", "break", "end"]


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
                if source[i] == ":":
                    try:
                        if source[i + 1] == "=":
                            if not (source[i + 2] in whitespace and
                                    source[i - 1] in whitespace):
                                msg = (
                                    "assignment operator and its operands must"
                                    " be separated by whitespace")
                                self.lasttoken = "error"
                                yield Token(name="ERROR", value=msg,
                                            source_pos=SourcePosition(
                                                idx=self.idx,
                                                lineno=self.lineno,
                                                colno=self.colno))
                                break
                            yield Token(name=":=", value=":=",
                                        source_pos=SourcePosition(
                                            idx=self.idx,
                                            lineno=self.lineno,
                                            colno=self.colno))
                            self.lasttoken = ":="
                            self.colno += 2
                            i += 2
                            continue
                    except IndexError:
                        msg = (
                            "assignment operator and its operands must "
                            "be separated by whitespace")
                        self.lasttoken = "error"
                        yield Token(name="ERROR", value=msg,
                                    source_pos=SourcePosition(
                                        idx=self.idx,
                                        lineno=self.lineno,
                                        colno=self.colno))
                        break
                    else:
                        self.lasttoken = ":"
                        yield Token(name=":", value=":",
                                    source_pos=SourcePosition(
                                        idx=self.idx,
                                        lineno=self.lineno,
                                        colno=self.colno))
                        self.colno += 1
                        i += 1
                        continue
                elif source[i] == ".":
                    try:
                        if (source[i + 1] in whitespace or
                                source[i - 1] in whitespace):
                            msg = "disconnected \".\""
                            self.lasttoken = "error"
                            yield Token(name="ERROR", value=msg,
                                        source_pos=SourcePosition(
                                            idx=self.idx,
                                            lineno=self.lineno,
                                            colno=self.colno))
                            break
                    except IndexError:
                        msg = "disconnected \".\""
                        self.lasttoken = "error"
                        yield Token(name="ERROR", value=msg,
                                    source_pos=SourcePosition(
                                        idx=self.idx,
                                        lineno=self.lineno,
                                        colno=self.colno))
                        break
                    self.lasttoken = "."
                    yield Token(name=".", value=".",
                                source_pos=SourcePosition(idx=self.idx,
                                                          lineno=self.lineno,
                                                          colno=self.colno))
                    self.colno += 1
                    i += 1
                    continue
                elif source[i] == ",":
                    self.lasttoken = ","
                    yield Token(name=",", value=",",
                                source_pos=SourcePosition(idx=self.idx,
                                                          lineno=self.lineno,
                                                          colno=self.colno))
                    self.colno += 1
                    i += 1
                    continue
                elif source[i] == ";":
                    self.lasttoken = ";"
                    yield Token(name=";", value=";",
                                source_pos=SourcePosition(idx=self.idx,
                                                          lineno=self.lineno,
                                                          colno=self.colno))
                    self.colno += 1
                    i += 1
                    continue
                elif source[i] == "(":
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
                elif source[i] == "[":
                    self.lasttoken = "["
                    yield Token(name="[", value="[",
                                source_pos=SourcePosition(idx=self.idx,
                                                          lineno=self.lineno,
                                                          colno=self.colno))
                    self.colno += 1
                    i += 1
                    continue
                elif source[i] == "]":
                    self.lasttoken = "]"
                    yield Token(name="]", value="]",
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
                            if source[i + 1] == "+":
                                if (source[i + 2] in whitespace and
                                        source[i - 1] in whitespace):
                                    yield Token(name="++", value="++",
                                                source_pos=SourcePosition(
                                                    idx=self.idx,
                                                    lineno=self.lineno,
                                                    colno=self.lineno))
                                    self.lasttoken = "++"
                                    self.colno += 2
                                    i += 2
                                    continue
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
                    try:
                        if not (source[i + 1] in whitespace and source[i - 1]
                           in whitespace):
                            if source[i + 1] == "-":
                                if (source[i + 2] in whitespace and
                                        source[i - 1] in whitespace):
                                    yield Token(name="--", value="--",
                                                source_pos=SourcePosition(
                                                    idx=self.idx,
                                                    lineno=self.lineno,
                                                    colno=self.lineno))
                                    self.lasttoken = "--"
                                    self.colno += 2
                                    i += 2
                                    continue
                            else:
                                yield Token(name="NEG", value="NEG",
                                            source_pos=SourcePosition(
                                                idx=self.idx,
                                                lineno=self.lineno,
                                                colno=self.lineno))
                                self.lasttoken = "NEG"
                                self.colno += 1
                                i += 1
                                continue
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
                                "binary operator and its operands must "
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
                                "binary operator and its operands must "
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
                                "binary operator and its operands must "
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
                                    "binary operator and its operands must "
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
                            self.lasttoken = "=="
                            self.colno += 2
                            i += 2
                            continue
                        else:
                            if not (source[i + 1] in whitespace and
                                    source[i - 1] in whitespace):
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
                            yield Token(name="=", value="=",
                                        source_pos=SourcePosition(
                                            idx=self.idx,
                                            lineno=self.lineno,
                                            colno=self.colno))
                            self.lasttoken = "="
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
                                    "binary operator and its operands must "
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
                            self.lasttoken = "!="
                            self.colno += 2
                            i += 2
                            continue
                        elif source[i + 1] not in whitespace:
                            yield Token(name="!",
                                        value="!",
                                        source_pos=SourcePosition(
                                            idx=self.idx,
                                            lineno=self.lineno,
                                            colno=self.colno))
                            self.lasttoken = "!"
                            self.colno += 1
                            i += 1
                            continue
                        else:
                            msg = ("unary operator must be "
                                   "prepended to its operand")
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
                                    "binary operator and its operands must "
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
                            self.lasttoken = "<="
                            self.colno += 2
                            i += 2
                            continue
                        else:
                            if not (source[i + 1] in whitespace and
                                    source[i - 1] in whitespace):
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
                            yield Token(name="<", value="<",
                                        source_pos=SourcePosition(
                                            idx=self.idx,
                                            lineno=self.lineno,
                                            colno=self.colno))
                            self.lasttoken = "<"
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
                                    "binary operator and its operands must "
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
                            self.lasttoken = ">="
                            self.colno += 2
                            i += 2
                            continue
                        else:
                            if not (source[i + 1] in whitespace and
                                    source[i - 1] in whitespace):
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
                            yield Token(name=">", value=">",
                                        source_pos=SourcePosition(
                                            idx=self.idx,
                                            lineno=self.lineno,
                                            colno=self.colno))
                            self.lasttoken = ">"
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
                                "binary operator and its operands must "
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
                                "binary operator and its operands must "
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
                    k = 2
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
            else:
                j = i
                k = 0
                while not (source[j] in whitespace or
                           source[j] in symbols):
                    value.append(source[j])
                    j += 1
                    k += 1
                    try:
                        source[j]
                    except IndexError:
                        break
                iden = "".join(value)
                if iden in reserved:
                    if iden == "fetch":
                        self.lasttoken = "fetch"
                        yield Token(name="FETCH", value=iden,
                                    source_pos=SourcePosition(
                                        idx=self.idx,
                                        lineno=self.lineno,
                                        colno=self.colno))
                    elif iden == "func":
                        self.lasttoken = "func"
                        yield Token(name="FUNC", value=iden,
                                    source_pos=SourcePosition(
                                        idx=self.idx,
                                        lineno=self.lineno,
                                        colno=self.colno))
                    elif iden == "where":
                        self.lasttoken = "where"
                        yield Token(name="WHERE", value=iden,
                                    source_pos=SourcePosition(
                                        idx=self.idx,
                                        lineno=self.lineno,
                                        colno=self.colno))
                    elif iden == "if":
                        self.lasttoken = "if"
                        yield Token(name="IF", value=iden,
                                    source_pos=SourcePosition(
                                        idx=self.idx,
                                        lineno=self.lineno,
                                        colno=self.colno))
                    elif iden == "then":
                        self.lasttoken = "then"
                        yield Token(name="THEN", value=iden,
                                    source_pos=SourcePosition(
                                        idx=self.idx,
                                        lineno=self.lineno,
                                        colno=self.colno))
                    elif iden == "else":
                        self.lasttoken = "else"
                        yield Token(name="ELSE", value=iden,
                                    source_pos=SourcePosition(
                                        idx=self.idx,
                                        lineno=self.lineno,
                                        colno=self.colno))
                    elif iden == "for":
                        self.lasttoken = "for"
                        yield Token(name="FOR", value=iden,
                                    source_pos=SourcePosition(
                                        idx=self.idx,
                                        lineno=self.lineno,
                                        colno=self.colno))
                    elif iden == "end":
                        self.lasttoken = "end"
                        yield Token(name="ENDLOOP", value=iden,
                                    source_pos=SourcePosition(
                                        idx=self.idx,
                                        lineno=self.lineno,
                                        colno=self.colno))
                    elif iden == "break":
                        self.lasttoken = "break"
                        yield Token(name="BREAK", value=iden,
                                    source_pos=SourcePosition(
                                        idx=self.idx,
                                        lineno=self.lineno,
                                        colno=self.colno))
                else:
                    self.lasttoken = "identifier"
                    yield Token(name="IDENTIFIER", value=iden,
                                source_pos=SourcePosition(
                                    idx=self.idx,
                                    lineno=self.lineno,
                                    colno=self.colno))
                value = []
                i = j
                self.colno += k
        if self.lasttoken in insertend:
            self.lasttoken = "END"
            yield Token(name="END", value="END",
                        source_pos=SourcePosition(
                            idx=self.idx,
                            lineno=self.lineno,
                            colno=self.colno))


lexer = Lexer()
