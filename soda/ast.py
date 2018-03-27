from rpython.rlib.runicode import str_decode_utf_8
from rply.token import BaseBox
from soda import bytecode
from soda.objects import SodaInt, SodaString, SodaFunction


class Node(BaseBox):
    pass


class List(Node):
    def __init__(self, item):
        self.items = []
        self.items.append(item)

    def append(self, item):
        self.items.append(item)

    def get(self):
        return self.items


class String(Node):
    def __init__(self, value, package, line, col):
        string = value.getstr()
        iden, trash = str_decode_utf_8(string, len(string), "strict", True)
        self.value = iden
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


class Variable(Node):
    def __init__(self, value, package, line, col):
        string = value.getstr()
        iden, trash = str_decode_utf_8(string, len(string), "strict", True)
        self.value = iden
        self.package = package
        self.line = line
        self.col = col

    def compile(self, compiler):
        compiler.emit(bytecode.LOAD_VAR,
                      compiler.variables.get(self.value, -1),
                      self.package, self.line, self.col)


class RegisterVariable(Node):
    def __init__(self, value, package, line, col):
        string = value.getstr()
        iden, trash = str_decode_utf_8(string, len(string), "strict", True)
        self.value = iden
        self.package = package
        self.line = line
        self.col = col

    def compile(self, compiler):
        compiler.emit(bytecode.STORE_VAR,
                      compiler.register_variable(self.value),
                      self.package, self.line, self.col)


class Assignment(Node):
    def __init__(self, idens, exprs, package, line, col):
        self.idens = idens
        self.exprs = exprs
        self.package = package
        self.line = line
        self.col = col

    def compile(self, compiler):
        exprlist = self.exprs.get()
        exprlist.reverse()
        for expr in exprlist:
            expr.compile(compiler)
        for iden in self.idens.get():
            iden.compile(compiler)


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


class Function(Node):
    def __init__(self, name, params, body, returnstatement,
                 package, line, col):
        string = name.getstr()
        iden, trash = str_decode_utf_8(string, len(string), "strict", True)
        self.name = iden
        self.params = []
        self.body = body
        self.returnstatement = returnstatement
        self.package = package
        self.line = line
        self.col = col
        self.compiler = bytecode.Compiler()
        for param in params:
            string = param.getstr()
            iden, trash = str_decode_utf_8(string, len(string), "strict", True)
            self.params.append(iden)

    def compile(self, compiler):
        if self.body is not None:
            for statement in self.body.get():
                statement.compile(self.compiler)
        self.returnstatement.compile(self.compiler)
        function = SodaFunction(name=self.name, arity=len(self.params),
                                package=self.package, line=self.line,
                                col=self.col)
        compiler.register_function(function)
        self.compiler.register_function(function)


class ReturnStatement(Node):
    def __init__(self, value, package, line, col):
        self.value = value
        self.package = package
        self.line = line
        self.col = col

    def compile(self, compiler):
        self.value.compile(compiler)
        compiler.emit(bytecode.RETURN, 0,
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
