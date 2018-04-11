from soda import bytecode
from soda.objects import SodaArray
from soda.errors import sodaError
from rpython.rlib import jit
import os

driver = jit.JitDriver(greens=["pc", "iteridx", "code",
                               "positions", "bc"],
                       reds=["frame"],
                       is_recursive=True)


class Frame(object):
    def __init__(self, bc):
        self.valuestack = []
        self.variables = [None] * bc.numvars
        self.valuestack_pos = 0

    def push(self, value):
        self.valuestack.append(value)

    def pop(self):
        return self.valuestack.pop()


def run(frame, bc):
    code = bc.code
    positions = bc.positions
    pc = 0
    iteridx = 0
    while pc < len(bc.code):
        driver.jit_merge_point(pc=pc, iteridx=iteridx, code=code,
                               positions=positions, bc=bc, frame=frame)
        c = code[pc]
        arg = code[pc + 1]
        package, line, col = positions[pc]
        pc += 2
        if c == bytecode.DROP_CONST:
            frame.pop()
        elif c == bytecode.LOAD_CONST:
            const = bc.constants[arg]
            frame.push(const)
        elif c == bytecode.LOAD_VAR:
            if arg == -1:
                sodaError(package, line, col,
                          "cannot evaluate undeclared variable")
            var = frame.variables[arg]
            frame.push(var)
        elif c == bytecode.STORE_VAR:
            package = package
            line = line
            col = col
            value = frame.pop()
            frame.variables[arg] = value
        elif c == bytecode.STOR_ARRAY:
            package = package
            line = line
            col = col
            items = []
            for i in range(0, arg):
                items.append(frame.pop())
            sa = SodaArray(items)
            frame.push(sa)
        elif c == bytecode.NEG:
            operand = frame.pop()
            if not operand.isint():
                try:
                    operand = operand.toint()
                except Exception:
                    sodaError(package, line, col,
                              "cannot negate non-integer type")
            result = operand.neg()
            frame.push(result)
        elif c == bytecode.ADD:
            right = frame.pop()
            left = frame.pop()
            if not right.isint():
                try:
                    right = right.toint()
                except Exception:
                    sodaError(package, line, col,
                              "cannot add non-integer types")
            if not left.isint():
                try:
                    left = left.toint()
                except Exception:
                    sodaError(package, line, col,
                              "cannot add non-integer types")
            result = right.add(left)
            frame.push(result)
        elif c == bytecode.CONCAT:
            right = frame.pop()
            left = frame.pop()
            if not left.isstr():
                try:
                    left = left.tostr()
                except Exception:
                    sodaError(package, line, col,
                              "cannot concatenate non-string types")
            if not right.isstr():
                try:
                    right = right.tostr()
                except Exception:
                    sodaError(package, line, col,
                              "cannot concatenate non-string types")
            result = right.concat(left)
            frame.push(result)
        elif c == bytecode.DIFF:
            right = frame.pop()
            left = frame.pop()
            if not left.isstr():
                try:
                    left = left.tostr()
                except Exception:
                    sodaError(package, line, col,
                              "cannot find string difference of non-string"
                              " types")
            if not right.isstr():
                try:
                    right = right.tostr()
                except Exception:
                    sodaError(package, line, col,
                              "cannot find string difference of non-string"
                              " types")
            result = right.diff(left)
            frame.push(result)
        elif c == bytecode.SUB:
            right = frame.pop()
            left = frame.pop()
            if not right.isint():
                try:
                    right = right.toint()
                except Exception:
                    sodaError(package, line, col,
                              "cannot subtract non-integer types")
            if not left.isint():
                try:
                    left = left.toint()
                except Exception:
                    sodaError(package, line, col,
                              "cannot subtract non-integer types")
            result = right.sub(left)
            frame.push(result)
        elif c == bytecode.MUL:
            right = frame.pop()
            left = frame.pop()
            if not right.isint():
                try:
                    right = right.toint()
                except Exception:
                    sodaError(package, line, col,
                              "cannot multiply non-integer types")
            if not left.isint():
                try:
                    left = left.toint()
                except Exception:
                    sodaError(package, line, col,
                              "cannot multiply non-integer types")
            result = right.mul(left)
            frame.push(result)
        elif c == bytecode.DIV:
            right = frame.pop()
            left = frame.pop()
            if not right.isint():
                try:
                    right = right.toint()
                except Exception:
                    sodaError(package, line, col,
                              "cannot divide non-integer types")
            if not left.isint():
                try:
                    left = left.toint()
                except Exception:
                    sodaError(package, line, col,
                              "cannot divide non-integer types")
            try:
                result = right.div(left)
            except ZeroDivisionError:
                sodaError(package, line, col,
                          "cannot divide by zero")
                break
            frame.push(result)
        elif c == bytecode.MOD:
            right = frame.pop()
            left = frame.pop()
            if not right.isint():
                try:
                    right = right.toint()
                except Exception:
                    sodaError(package, line, col,
                              "cannot modulo non-integer types")
            if not left.isint():
                try:
                    left = left.toint()
                except Exception:
                    sodaError(package, line, col,
                              "cannot modulo non-integer types")
            try:
                result = right.mod(left)
            except ZeroDivisionError:
                sodaError(package, line, col,
                          "cannot modulo by zero")
                break
            frame.push(result)
        elif c == bytecode.POW:
            right = frame.pop()
            left = frame.pop()
            if not right.isint():
                try:
                    right = right.toint()
                except Exception:
                    sodaError(package, line, col,
                              "cannot exponentiate non-integer types")
            if not left.isint():
                try:
                    left = left.toint()
                except Exception:
                    sodaError(package, line, col,
                              "cannot exponentiate non-integer types")
            try:
                result = right.pow(left)
            except ValueError:
                sodaError(package, line, col,
                          "cannot exponentiate by a negative integer")
                break
            frame.push(result)
        elif c == bytecode.EQ:
            right = frame.pop()
            left = frame.pop()
            if left.isstr() and right.isstr() or left.isint()\
               and right.isint():
                result = right.eq(left)
                frame.push(result)
                continue
            try:
                right = right.toint()
                left = left.toint()
                result = right.eq(left)
                frame.push(result)
                continue
            except Exception:
                try:
                    right = right.tostr()
                    left = left.tostr()
                    result = right.eq(left)
                    frame.push(result)
                    continue
                except Exception:
                    sodaError(package, line, col,
                              "cannot compare arrays")
        elif c == bytecode.NE:
            right = frame.pop()
            left = frame.pop()
            if left.isstr() and right.isstr() or left.isint()\
               and right.isint():
                result = right.ne(left)
                frame.push(result)
                continue
            try:
                right = right.toint()
                left = left.toint()
                result = right.ne(left)
                frame.push(result)
                continue
            except Exception:
                try:
                    right = right.tostr()
                    left = left.tostr()
                    result = right.ne(left)
                    frame.push(result)
                    continue
                except Exception:
                    sodaError(package, line, col,
                              "cannot compare arrays")
        elif c == bytecode.GT:
            right = frame.pop()
            left = frame.pop()
            if left.isstr() and right.isstr() or left.isint()\
               and right.isint():
                result = right.gt(left)
                frame.push(result)
                continue
            try:
                right = right.toint()
                left = left.toint()
                result = right.gt(left)
                frame.push(result)
                continue
            except Exception:
                try:
                    right = right.tostr()
                    left = left.tostr()
                    result = right.gt(left)
                    frame.push(result)
                    continue
                except Exception:
                    sodaError(package, line, col,
                              "cannot compare arrays")
        elif c == bytecode.LT:
            right = frame.pop()
            left = frame.pop()
            if left.isstr() and right.isstr() or left.isint()\
               and right.isint():
                result = right.lt(left)
                frame.push(result)
                continue
            try:
                right = right.toint()
                left = left.toint()
                result = right.lt(left)
                frame.push(result)
                continue
            except Exception:
                try:
                    right = right.tostr()
                    left = left.tostr()
                    result = right.lt(left)
                    frame.push(result)
                    continue
                except Exception:
                    sodaError(package, line, col,
                              "cannot compare arrays")
        elif c == bytecode.GE:
            right = frame.pop()
            left = frame.pop()
            if left.isstr() and right.isstr() or left.isint()\
               and right.isint():
                result = right.ge(left)
                frame.push(result)
                continue
            try:
                right = right.toint()
                left = left.toint()
                result = right.ge(left)
                frame.push(result)
                continue
            except Exception:
                try:
                    right = right.tostr()
                    left = left.tostr()
                    result = right.ge(left)
                    frame.push(result)
                    continue
                except Exception:
                    sodaError(package, line, col,
                              "cannot compare arrays")
        elif c == bytecode.LE:
            right = frame.pop()
            left = frame.pop()
            if left.isstr() and right.isstr() or left.isint()\
               and right.isint():
                result = right.le(left)
                frame.push(result)
                continue
            try:
                right = right.toint()
                left = left.toint()
                result = right.le(left)
                frame.push(result)
                continue
            except Exception:
                try:
                    right = right.tostr()
                    left = left.tostr()
                    result = right.le(left)
                    frame.push(result)
                    continue
                except Exception:
                    sodaError(package, line, col,
                              "cannot compare arrays")
        elif c == bytecode.AND:
            right = frame.pop()
            left = frame.pop()
            if not left.isstr():
                try:
                    left = left.tostr()
                except Exception:
                    sodaError(package, line, col,
                              "cannot compare arrays")
            if not right.isstr():
                try:
                    right = right.tostr()
                except Exception:
                    sodaError(package, line, col,
                              "cannot compare arrays")
            result = right.land(left)
            frame.push(result)
        elif c == bytecode.OR:
            right = frame.pop()
            left = frame.pop()
            if not left.isstr():
                try:
                    left = left.tostr()
                except Exception:
                    sodaError(package, line, col,
                              "cannot compare arrays")
            if not right.isstr():
                try:
                    right = right.tostr()
                except Exception:
                    sodaError(package, line, col,
                              "cannot compare arrays")
            result = right.lor(left)
            frame.push(result)
        elif c == bytecode.NOT:
            operand = frame.pop()
            if not operand.isstr():
                try:
                    operand = operand.tostr()
                except Exception:
                    sodaError(package, line, col,
                              "cannot compare arrays")
            result = operand.lnot()
            frame.push(result)
        elif c == bytecode.RETURN:
            result = frame.pop()
            return result
        elif c == bytecode.CALL:
            if arg == -1:
                sodaError(package, line, col,
                          "cannot evaluate undeclared function")
            elif arg == -2:
                sodaError(package, line, col,
                          "number of arguments passed to function "
                          "must match number of expected parameters")
            function = bc.constants[arg]
            if unicode(function.name) == u"Print" and unicode(
                    function.package) == u"io":
                output = frame.pop().str()
                os.write(1, output)
                fbc = function.compiler.create_bytecode()
                frame.push(interpret(fbc))
            if unicode(function.name) == u"Error" and unicode(
                    function.package) == u"io":
                output = frame.pop().str()
                os.write(2, output)
                fbc = function.compiler.create_bytecode()
                frame.push(interpret(fbc))
            else:
                arglist = []
                if function.isvariadic:
                    function.numargs = len(frame.valuestack)
                for i in range(0, function.numargs):
                    value = frame.pop()
                    arglist.append(value)
                function.evaluate_args(arglist)
                fbc = function.compiler.create_bytecode()
                try:
                    function.revert_state()
                    result = interpret(fbc)
                    frame.push(result)
                except RuntimeError:
                    sodaError(package, line, col,
                              "maximum recursion depth exceeded")
        elif c == bytecode.J_IF_TRUE:
            if not frame.pop().str() == "false":
                pc = arg
        elif c == bytecode.J_IF_FALSE:
            if frame.pop().str() == "false":
                pc = arg
        elif c == bytecode.ITERATE:
            array = frame.pop()
            try:
                keyval = array.getkey(iteridx)
                if keyval is None:
                    pc = arg
                    iteridx = 0
                else:
                    frame.push(keyval)
                    iteridx += 1
            except Exception:
                sodaError(package, line, col,
                          "cannot iterate non-array types")
        elif c == bytecode.SET_INDEX:
            expr = frame.pop()
            var = frame.pop()
            newval = frame.pop()
            try:
                var.setval(expr, newval)
            except Exception:
                sodaError(package, line, col,
                          "cannot mutate non-array types")
        elif c == bytecode.GET_INDEX:
            expr = frame.pop()
            var = frame.pop()
            try:
                result = var.getval(expr)
                frame.push(result)
            except IndexError:
                sodaError(package, line, col,
                          "string index out of range")
            except Exception:
                sodaError(package, line, col,
                          "cannot index integers")
        elif c == bytecode.JUMP:
            if arg == -3:
                sodaError(package, line, col,
                          "break statement outside loop")
            oldpc = pc
            pc = arg
            if pc < oldpc:
                driver.can_enter_jit(pc=pc, iteridx=iteridx, code=code,
                                     positions=positions, bc=bc, frame=frame)
        elif c == bytecode.LEN:
            length = frame.pop().length
            if length is not None:
                frame.push(length)
            else:
                sodaError(package, line, col,
                          "cannot find length of integer")
        else:
            sodaError("test", "-1", "-1", "unrecognized bytecode %s" % c)


def interpret(bc):
    frame = Frame(bc)
    result = run(frame, bc)
    return result
