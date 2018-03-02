from rply.token import BaseBox
from soda import bytecode
from soda.objects import SodaNumber, SodaString


class Node(BaseBox):
    pass


class StatementPair(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def compile(self, compiler):
        self.left.compile(compiler)
        self.right.compile(compiler)


class Statement(Node):
    def __init__(self, expr):
        self.expr = expr

    def compile(self, compiler):
        self.expr.compile(compiler)


class String(Node):
    def __init__(self, value):
        self.value = value

    def compile(self, compiler):
        ss = SodaString(self.value)
        compiler.emit(bytecode.LOAD_CONST, compiler.register_constant(ss))


class Number(Node):
    def __init__(self, value):
        self.value = value

    def compile(self, compiler):
        sn = SodaNumber(self.value)
        compiler.emit(bytecode.LOAD_CONST, compiler.register_constant(sn))


class BinOp(Node):
    def __init__(self, operator, left, right):
        self.left = left
        self.right = right
        self.operator = operator

    def compile(self, compiler):
        self.right.compile(compiler)
        self.left.compile(compiler)
        compiler.emit(bytecode.BINOP_CODE[self.operator])


class PutStatement(Node):
    def __init__(self, expr):
        self.expr = expr

    def compile(self, compiler):
        self.expr.compile(compiler)
        compiler.emit(bytecode.PUT)
