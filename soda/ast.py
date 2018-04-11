from rpython.rlib.runicode import str_decode_utf_8
from rply.token import BaseBox
from soda import bytecode
from soda.errors import sodaError
from soda.objects import SodaInt, SodaString, SodaFunction, SodaDummy


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

    def reverse(self):
        self.items.reverse()
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


class Expression(Node):
    def __init__(self, value):
        self.value = value

    def compile(self, compiler):
        self.value.compile(compiler)
        compiler.emit(bytecode.DROP_CONST, 0,
                      "", "", "")


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


class Array(Node):
    def __init__(self, items, package, line, col):
        self.itemlist = items
        self.package = package
        self.line = line
        self.col = col

    def compile(self, compiler):
        for item in self.itemlist:
            item.compile(compiler)
        compiler.emit(bytecode.STOR_ARRAY, len(self.itemlist),
                      self.package, self.line, self.col)


class If(Node):
    def __init__(self, cond, body, elsestatement, package, line, col):
        self.cond = cond
        self.body = body
        self.elsestatement = elsestatement
        self.package = package
        self.line = line
        self.col = col

    def compile(self, compiler):
        self.cond.compile(compiler)
        compiler.emit(bytecode.J_IF_TRUE, 0, self.package,
                      self.line, self.col)
        jumppos = len(compiler.stack) - 1
        self.elsestatement.compile(compiler)
        compiler.emit(bytecode.JUMP, 0, self.package,
                      self.line, self.col)
        compiler.stack[jumppos] = len(compiler.stack)
        jumppos = len(compiler.stack) - 1
        for statement in self.body:
            statement.compile(compiler)
        compiler.stack[jumppos] = len(compiler.stack)


class For(Node):
    def __init__(self, init, cond, post, body, package, line, col):
        self.init = init
        self.cond = cond
        self.post = post
        self.body = body
        self.package = package
        self.line = line
        self.col = col

    def compile(self, compiler):
        self.init.compile(compiler)
        initpos = len(compiler.stack)
        self.cond.compile(compiler)
        compiler.emit(bytecode.J_IF_FALSE, 0, self.package,
                      self.line, self.col)
        postpos = len(compiler.stack) - 1
        for statement in self.body:
            statement.compile(compiler)
        self.post.compile(compiler)
        compiler.emit(bytecode.JUMP, initpos, self.package,
                      self.line, self.col)
        compiler.stack[postpos] = len(compiler.stack)
        for i in range(initpos, len(compiler.stack)):
            if compiler.stack[i] == -3:
                compiler.stack[i] = len(compiler.stack)


class While(Node):
    def __init__(self, cond, body, package, line, col):
        self.cond = cond
        self.body = body
        self.package = package
        self.line = line
        self.col = col

    def compile(self, compiler):
        initpos = len(compiler.stack)
        self.cond.compile(compiler)
        compiler.emit(bytecode.J_IF_FALSE, 0, self.package,
                      self.line, self.col)
        postpos = len(compiler.stack) - 1
        for statement in self.body:
            statement.compile(compiler)
        compiler.emit(bytecode.JUMP, initpos, self.package,
                      self.line, self.col)
        compiler.stack[postpos] = len(compiler.stack)
        for i in range(initpos, len(compiler.stack)):
            if compiler.stack[i] == -3:
                compiler.stack[i] = len(compiler.stack)


class Iterate(Node):
    def __init__(self, value, expr, body, package, line, col):
        string = value.getstr()
        iden, trash = str_decode_utf_8(string, len(string), "strict", True)
        self.value = iden
        self.expr = expr
        self.body = body
        self.package = package
        self.line = line
        self.col = col

    def compile(self, compiler):
        initpos = len(compiler.stack)
        self.expr.compile(compiler)
        compiler.emit(bytecode.ITERATE, 0, self.package,
                      self.line, self.col)
        postpos = len(compiler.stack) - 1
        compiler.emit(bytecode.STORE_VAR,
                      compiler.register_variable(self.value, self.package),
                      self.package, self.line, self.col)
        for statement in self.body:
            statement.compile(compiler)
        compiler.emit(bytecode.JUMP, initpos, self.package,
                      self.line, self.col)
        compiler.stack[postpos] = len(compiler.stack)
        for i in range(initpos, len(compiler.stack)):
            if compiler.stack[i] == -3:
                compiler.stack[i] = len(compiler.stack)


class Break(Node):
    def __init__(self, package, line, col):
        self.package = package
        self.line = line
        self.col = col

    def compile(self, compiler):
        compiler.emit(bytecode.JUMP, -3,
                      self.package, self.line, self.col)


class Variable(Node):
    def __init__(self, value, reference, package, line, col):
        string = value.getstr()
        iden, trash = str_decode_utf_8(string, len(string), "strict", True)
        self.value = iden
        if reference is not None:
            string = reference.getstr()
            ref, trash = str_decode_utf_8(string, len(string), "strict", True)
        else:
            ref = unicode(package)
        self.reference = ref
        self.package = package
        self.line = line
        self.col = col

    def compile(self, compiler):
        compiler.emit(bytecode.LOAD_VAR,
                      compiler.variables.get(self.value + self.reference, -1),
                      self.package, self.line, self.col)


class SetIndex(Node):
    def __init__(self, var, idx, package, line, col):
        self.var = var
        self.idx = idx
        self.package = package
        self.line = line
        self.col = col

    def compile(self, compiler):
        self.var.compile(compiler)
        self.idx.compile(compiler)
        compiler.emit(bytecode.SET_INDEX, 0,
                      self.package, self.line, self.col)


class GetIndex(Node):
    def __init__(self, var, idx, package, line, col):
        self.var = var
        self.idx = idx
        self.package = package
        self.line = line
        self.col = col

    def compile(self, compiler):
        self.var.compile(compiler)
        self.idx.compile(compiler)
        compiler.emit(bytecode.GET_INDEX, 0,
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
                      compiler.register_variable(self.value, self.package),
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
        self.params = params
        self.body = body
        self.returnstatement = returnstatement
        self.package = package
        self.line = line
        self.col = col
        self.compiler = bytecode.Compiler()

    def compile(self, compiler):
        function = SodaFunction(name=self.name, arity=len(self.params),
                                compiler=self.compiler, package=self.package,
                                line=self.line, col=self.col)
        compiler.register_function(function)
        for constant in compiler.constants:
            if isinstance(constant, SodaFunction):
                self.compiler.register_function(constant)
        sd = SodaDummy()
        for i in range(0, function.arity):
            self.compiler.emit(bytecode.LOAD_CONST,
                               self.compiler.register_constant(sd),
                               self.package, self.line, self.col)
        for param in self.params:
            assert isinstance(param, RegisterVariable)
            if param.value == unicode("vargs"):
                if self.params.index(param) != len(self.params) - 1:
                    sodaError(self.package, self.line, self.col,
                              "vargs must be final parameter in "
                              "function declaration")
                function.isvariadic = True
            param.compile(self.compiler)
        for statement in self.body:
            statement.compile(self.compiler)
        self.returnstatement.compile(self.compiler)


class Call(Node):
    def __init__(self, name, reference, exprlist, package, line, col):
        string = name.getstr()
        iden, trash = str_decode_utf_8(string, len(string), "strict", True)
        self.name = iden
        if reference is not None:
            string = reference.getstr()
            ref, trash = str_decode_utf_8(string, len(string), "strict", True)
        else:
            ref = unicode(package)
        self.reference = ref
        self.exprlist = exprlist
        self.package = package
        self.line = line
        self.col = col

    def compile(self, compiler):
        for expr in self.exprlist:
            expr.compile(compiler)
        idx = compiler.functions.get(self.name + self.reference, -1)
        if not idx == -1:
            function = compiler.constants[idx]
            if not function.isvariadic:
                if not len(self.exprlist) == function.arity:
                    idx = -2
            else:
                if not len(self.exprlist) >= function.arity - 1:
                    idx = -2
        compiler.emit(bytecode.CALL, idx,
                      self.package, self.line, self.col)


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


class Len(Node):
    def __init__(self, value, package, line, col):
        self.value = value
        self.package = package
        self.line = line
        self.col = col

    def compile(self, compiler):
        self.value.compile(compiler)
        compiler.emit(bytecode.LEN, 0,
                      self.package, self.line, self.col)
