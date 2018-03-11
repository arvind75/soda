LOAD_CONST = 1
ADD = 2
CONCAT = 3
DIFF = 4
SUB = 5
MUL = 6
DIV = 7
MOD = 8
POW = 9
EQ = 10
NE = 11
GT = 12
LT = 13
GE = 14
LE = 15
AND = 16
OR = 17
PUT = 18

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
    "|": OR
}

# names for dumping bc to terminal
# spacing is odd because rpython disallows conventional string formatting
NAMES = {
    LOAD_CONST: "LOAD_CONST",
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
    PUT: "       PUT",
}


class Compiler(object):
    def __init__(self):
        self.stack = []
        self.positions = []
        self.constants = []

    def register_constant(self, value):
        self.constants.append(value)
        return len(self.constants) - 1

    def emit(self, code, arg=0, package="", line="-1", col="-1"):
        self.stack.append(code)
        self.stack.append(arg)
        self.positions.append(package)
        self.positions.append(line)
        self.positions.append(col)

    def create_bytecode(self):
        return Bytecode(self.stack, self.positions, self.constants[:])


class Bytecode(object):
    def __init__(self, code, positions, constants):
        self.code = code
        self.positions = positions
        self.constants = constants

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
