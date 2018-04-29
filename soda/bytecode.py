# Phillip Wells
# CSCI-200 Algorithm Analysis

# bytecode.py defines the bytecode and
# compiler for soda

from soda.errors import sodaError
from rpython.rlib.rbigint import rbigint
from rpython.rlib.runicode import str_decode_utf_8
from soda.objects import SodaArray, SodaString, SodaInt

DROP_CONST = 0
LOAD_CONST = 1
LOAD_VAR = 2
STORE_VAR = 3
STOR_ARRAY = 4
ADD = 5
CONCAT = 6
DIFF = 7
SUB = 8
MUL = 9
DIV = 10
MOD = 11
POW = 12
EQ = 13
NE = 14
GT = 15
LT = 16
GE = 17
LE = 18
AND = 19
OR = 20
NEG = 21
NOT = 22
RETURN = 23
CALL = 24
JUMP = 25
J_IF_TRUE = 26
J_IF_FALSE = 27
ITERATE = 28
GET_INDEX = 29
SET_INDEX = 30
LEN = 31
CHARS = 32
WORDS = 33
LINES = 34

BINOP_CODE = {
    "+": ADD,
    "++": CONCAT,
    "--": DIFF,
    "-": SUB,
    "*": MUL,
    "/": DIV,
    "%": MOD,
    "^": POW,
    "==": EQ,
    "!=": NE,
    "<": LT,
    ">": GT,
    "<=": LE,
    ">=": GE,
    "&": AND,
    "|": OR,
}

UNOP_CODE = {
    "NEG": NEG,
    "!": NOT
}

# names for dumping bc to terminal
# spacing is odd because rpython disallows conventional string formatting
NAMES = {
    DROP_CONST: "DROP_CONST",
    LOAD_CONST: "LOAD_CONST",
    LOAD_VAR: "  LOAD_VAR",
    STORE_VAR: " STORE_VAR",
    STOR_ARRAY: "STOR_ARRAY",
    ADD: "       ADD",
    CONCAT: "    CONCAT",
    DIFF: "      DIFF",
    SUB: "       SUB",
    MUL: "       MUL",
    DIV: "       DIV",
    MOD: "       MOD",
    POW: "       POW",
    EQ: "        EQ",
    NE: "        NE",
    LT: "        LT",
    GT: "        GT",
    LE: "        LE",
    GE: "        GE",
    AND: "       AND",
    OR: "        OR",
    NEG: "       NEG",
    NOT: "       NOT",
    RETURN: "    RETURN",
    CALL: "      CALL",
    JUMP: "      JUMP",
    J_IF_TRUE: " J_IF_TRUE",
    J_IF_FALSE: "J_IF_FALSE",
    ITERATE: "   ITERATE",
    GET_INDEX: " GET_INDEX",
    SET_INDEX: " SET_INDEX",
    LEN: "       LEN",
    CHARS: "     CHARS",
    WORDS: "     WORDS",
    LINES: "     LINES"
}


class Compiler(object):
    def __init__(self):
        self.stack = []
        self.constants = []
        self.positions = []
        self.variables = {}
        self.functions = {}

    def register_constant(self, value):
        self.constants.append(value)
        return len(self.constants) - 1

    def register_variable(self, name, package):
        package = unicode(package)
        try:
            return self.variables[name + package]
        except KeyError:
            self.variables[name + package] = len(self.variables)
            return len(self.variables) - 1

    def register_function(self, function):
        package = unicode(function.package)
        try:
            self.functions[function.name + package]
            sodaError(function.package, function.line, function.col,
                      "redeclaration of function \"%s\"" % function.name.encode
                      ("utf-8"))
        except KeyError:
            self.functions[function.name +
                           package] = self.register_constant(function)

    def emit(self, code, arg=0, package="", line="-1", col="-1"):
        self.stack.append(code)
        self.stack.append(arg)
        self.positions.append((package, line, col))
        self.positions.append(("", "", ""))

    def create_bytecode(self):
        return Bytecode(self.stack, self.positions, self.constants[:],
                        len(self.variables))


class Bytecode(object):
    def __init__(self, code, positions, constants, numvars):
        self.code = code
        self.positions = positions
        self.constants = constants
        self.numvars = numvars
        self.textarrays = []

    def dump(self):
        formatted = []
        for i in range(0, len(self.code), 2):
            opcode = NAMES[self.code[i]]
            argument = str(self.code[i + 1])
            formatted.append("%s %s\n" % (opcode, argument))
        return "".join(formatted)

    def create_arrays(self, text):
        self.textarrays = []
        chars, words, lines = [], [], []
        wordbuffer, linebuffer = [], []
        i, j, k = 0, 0, 0
        a = rbigint()
        text, trash = str_decode_utf_8(text, len(text), "strict", True)
        for char in text:
            if char == " " and wordbuffer != []:
                word = u"".join(wordbuffer)
                words.append(SodaInt(a.fromint(j)))
                words.append(SodaString(word))
                wordbuffer = []
                j += 1
                chars.append(SodaInt(a.fromint(i)))
                chars.append(SodaString(char))
                linebuffer.append(char)
                i += 1
            elif char == "\n" and linebuffer != []:
                line = u"".join(linebuffer)
                lines.append(SodaInt(a.fromint(k)))
                lines.append(SodaString(line))
                linebuffer = []
                k += 1
                if not wordbuffer == []:
                    word = u"".join(wordbuffer)
                    words.append(SodaInt(a.fromint(j)))
                    words.append(SodaString(word))
                    wordbuffer = []
                    j += 1
                chars.append(SodaInt(a.fromint(i)))
                chars.append(SodaString(char))
                i += 1
            else:
                chars.append(SodaInt(a.fromint(i)))
                chars.append(SodaString(char))
                wordbuffer.append(char)
                linebuffer.append(char)
                i += 1
        if not wordbuffer == []:
            word = u"".join(wordbuffer)
            words.append(SodaInt(a.fromint(j)))
            words.append(SodaString(word))
        if not linebuffer == []:
            line = u"".join(linebuffer)
            lines.append(SodaInt(a.fromint(k)))
            lines.append(SodaString(line))
        self.textarrays.append(SodaArray(chars))
        self.textarrays.append(SodaArray(words))
        self.textarrays.append(SodaArray(lines))


def compile_ast(ast_node):
    compiler = Compiler()
    for node in ast_node.get():
        node.compile(compiler)
    return compiler.create_bytecode()
