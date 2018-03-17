LOAD_CONST = 1
LOAD_VAR = 2
ADD = 3
CONCAT = 4
DIFF = 5
SUB = 6
MUL = 7
DIV = 8
MOD = 9
POW = 10
EQ = 11
NE = 12
GT = 13
LT = 14
GE = 15
LE = 16
AND = 17
OR = 18
NEG = 19
NOT = 20
ASSIGN = 21
PUT = 22

BINOP_CODE = {
    "+": ADD,
    "++": CONCAT,
    "--": DIFF,
    "-": SUB,
    "*": MUL,
    "/": DIV,
    "%": MOD,
    "^": POW,
    "=": EQ,
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
    LOAD_CONST: "LOAD_CONST",
    LOAD_VAR: "  LOAD_VAR",
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
    ASSIGN: "    ASSIGN",
    PUT: "       PUT",
}


class Compiler(object):
    def __init__(self):
        self.stack = []
        self.positions = []
        self.constants = []
        self.variables = []
        self.varpositions = {}

    def register_constant(self, value):
        self.constants.append(value)
        return len(self.constants) - 1

    def register_variable(self, name):
        try:
            return self.varpositions[name]
        except KeyError:
            self.varpositions[name] = len(self.variables)
            self.variables.append(name)
            return len(self.variables) - 1

    def emit(self, code, arg=0, package="", line="-1", col="-1"):
        self.stack.append(code)
        self.stack.append(arg)
        self.positions.append(package)
        self.positions.append(line)
        self.positions.append(col)

    def create_bytecode(self):
        return Bytecode(self.stack, self.positions, self.constants[:],
                        len(self.variables))


class Bytecode(object):
    def __init__(self, code, positions, constants, numvars):
        self.code = code
        self.positions = positions
        self.constants = constants
        self.numvars = numvars

    def dump(self):
        formatted = []
        for i in range(0, len(self.code), 2):
            opcode = NAMES[self.code[i]]
            argument = str(self.code[i + 1])
            formatted.append("%s %s\n" % (opcode, argument))
        return "".join(formatted)


def compile_ast(ast_node):
    compiler = Compiler()
    ast_node.compile(compiler)
    return compiler.create_bytecode()
