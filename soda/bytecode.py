LOAD_CONST = 1
ADD = 2
SUB = 3
MUL = 4
DIV = 5
MOD = 6
POW = 7
EQ = 8
NE = 9
GT = 10
LT = 11
GE = 12
LE = 13
AND = 14
OR = 15
PUT = 16

BINOP_CODE = {
    "+": ADD,
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
        self.constants = []

    def register_constant(self, value):
        self.constants.append(value)
        return len(self.constants) - 1

    def emit(self, code, arg=0):
        self.stack.append(code)
        self.stack.append(arg)

    def create_bytecode(self):
        return Bytecode(self.stack, self.constants[:])


class Bytecode(object):
    def __init__(self, code, constants):
        self.code = code
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
