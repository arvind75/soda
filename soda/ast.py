from rply.token import BaseBox
from soda import bytecode
from soda.objects import SodaInt, SodaString


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
    def __init__(self, value, package, line, col):
        self.value = value
        self.package = package
        self.line = line
        self.col = col

    def compile(self, compiler):
        ss = SodaString(self.value)
        compiler.emit(bytecode.LOAD_CONST, compiler.register_constant(ss),
                      self.package, self.line, self.col)


class Integer(Node):
    def __init__(self, value, package, line, col):
        self.value = value
        self.package = package
        self.line = line
        self.col = col

    def compile(self, compiler):
        si = SodaInt(self.value)
        compiler.emit(bytecode.LOAD_CONST, compiler.register_constant(si),
                      self.package, self.line, self.col)


class BinOp(Node):
    def __init__(self, operator, left, right, package, line, col):
        self.left = left
        self.right = right
        self.operator = operator
        self.package = package
        self.line = line
        self.col = col

    def compile(self, compiler):
        self.right.compile(compiler)
        self.left.compile(compiler)
        compiler.emit(bytecode.BINOP_CODE[self.operator], 0,
                      self.package, self.line, self.col)


class UnOp(Node):
    def __init__(self, operator, operand, package, line, col):
        self.operand = operand
        self.operator = operator
        self.package = package
        self.line = line
        self.col = col

    def compile(self, compiler):
        self.operand.compile(compiler)
        compiler.emit(bytecode.UNOP_CODE[self.operator], 0,
                      self.package, self.line, self.col)


class PutStatement(Node):
    def __init__(self, expr, package, line, col):
        self.expr = expr
        self.package = package
        self.line = line
        self.col = col

    def compile(self, compiler):
        self.expr.compile(compiler)
        compiler.emit(bytecode.PUT, 0, self.package,
                      self.line, self.col)
