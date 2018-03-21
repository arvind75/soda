LOAD_CONST = 1
LOAD_VAR = 2
STORE_VAR = 3
ADD = 4
CONCAT = 5
DIFF = 6
SUB = 7
MUL = 8
DIV = 9
MOD = 10
POW = 11
EQ = 12
NE = 13
GT = 14
LT = 15
GE = 16
LE = 17
AND = 18
OR = 19
NEG = 20
NOT = 21
RETURN = 22
PUT = 23

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
    STORE_VAR: " STORE_VAR",
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
    PUT: "       PUT",
}


class Compiler(object):
    def __init__(self):
        self.stack = []
        self.positions = []
        self.constants = []
        self.variables = {}
        self.functions = {}

    def register_constant(self, value):
        self.constants.append(value)
        return len(self.constants) - 1

    def register_variable(self, name):
        try:
            return self.variables[name]
        except KeyError:
            self.variables[name] = len(self.variables)
            return len(self.variables) - 1

    def register_function(self, function):
        self.functions[function.name] = self.register_constant(function)

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
