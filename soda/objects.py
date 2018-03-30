from rply.token import BaseBox
from rpython.rlib.rstring import UnicodeBuilder, replace
from rpython.rlib.rbigint import rbigint


class SodaObject(BaseBox):
    pass


class SodaDummy(SodaObject):
    def __init__(self):
        pass


class SodaString(SodaObject):
    def __init__(self, value):
        assert isinstance(value, unicode)
        self.value = value

    def concat(self, other):
        assert isinstance(other, SodaString)
        ustring = UnicodeBuilder()
        ustring.append(self.value)
        ustring.append(other.value)
        return SodaString(ustring.build())

    def diff(self, other):
        assert isinstance(other, SodaString)
        return SodaString(replace(self.value, other.value, u""))

    def eq(self, other):
        assert isinstance(other, SodaString)
        if (self.value == other.value):
            return SodaString(u"true")
        else:
            return SodaString(u"false")

    def ne(self, other):
        assert isinstance(other, SodaString)
        if (self.value != other.value):
            return SodaString(u"true")
        else:
            return SodaString(u"false")

    def gt(self, other):
        assert isinstance(other, SodaString)
        if (self.value > other.value):
            return SodaString(u"true")
        else:
            return SodaString(u"false")

    def lt(self, other):
        assert isinstance(other, SodaString)
        if (self.value < other.value):
            return SodaString(u"true")
        else:
            return SodaString(u"false")

    def ge(self, other):
        assert isinstance(other, SodaString)
        if (self.value >= other.value):
            return SodaString(u"true")
        else:
            return SodaString(u"false")

    def le(self, other):
        assert isinstance(other, SodaString)
        if (self.value <= other.value):
            return SodaString(u"true")
        else:
            return SodaString(u"false")

    def land(self, other):
        assert isinstance(other, SodaString)
        if (self.value == u"true" and other.value == u"true"):
            return SodaString(u"true")
        else:
            return SodaString(u"false")

    def lor(self, other):
        assert isinstance(other, SodaString)
        if (self.value == u"true" or other.value == u"true"):
            return SodaString(u"true")
        else:
            return SodaString(u"false")

    def lnot(self):
        if self.value == u"true":
            return SodaString(u"false")
        else:
            return SodaString(u"true")

    def isstr(self):
        return True

    def isint(self):
        return False

    def toint(self):
        a = rbigint()
        number = a.fromstr(str(self.value))
        return SodaInt(number)

    def tostr(self):
        return SodaString(self.value)

    def str(self):
        return self.value.encode("utf-8")


class SodaInt(SodaObject):
    def __init__(self, value):
        assert isinstance(value, rbigint)
        self.value = value

    def add(self, other):
        assert isinstance(other, SodaInt)
        return SodaInt(self.value.add(other.value))

    def sub(self, other):
        assert isinstance(other, SodaInt)
        return SodaInt(self.value.sub(other.value))

    def mul(self, other):
        assert isinstance(other, SodaInt)
        return SodaInt(self.value.mul(other.value))

    def div(self, other):
        assert isinstance(other, SodaInt)
        return SodaInt(self.value.floordiv(other.value))

    def mod(self, other):
        assert isinstance(other, SodaInt)
        return SodaInt(self.value.mod(other.value))

    def pow(self, other):
        assert isinstance(other, SodaInt)
        return SodaInt(self.value.pow(other.value))

    def eq(self, other):
        assert isinstance(other, SodaInt)
        if (self.value.eq(other.value)):
            return SodaString(u"true")
        else:
            return SodaString(u"false")

    def ne(self, other):
        assert isinstance(other, SodaInt)
        if (self.value.ne(other.value)):
            return SodaString(u"true")
        else:
            return SodaString(u"false")

    def gt(self, other):
        assert isinstance(other, SodaInt)
        if (self.value.gt(other.value)):
            return SodaString(u"true")
        else:
            return SodaString(u"false")

    def lt(self, other):
        assert isinstance(other, SodaInt)
        if (self.value.lt(other.value)):
            return SodaString(u"true")
        else:
            return SodaString(u"false")

    def ge(self, other):
        assert isinstance(other, SodaInt)
        if (self.value.ge(other.value)):
            return SodaString(u"true")
        else:
            return SodaString(u"false")

    def le(self, other):
        assert isinstance(other, SodaInt)
        if (self.value.le(other.value)):
            return SodaString(u"true")
        else:
            return SodaString(u"false")

    def neg(self):
        return SodaInt(self.value.neg())

    def isstr(self):
        return False

    def isint(self):
        return True

    def toint(self):
        return SodaInt(self.value)

    def tostr(self):
        return SodaString(self.str().decode("utf-8"))

    def str(self):
        s = self.value.str()
        return unicode(s).encode("utf-8")


class SodaFunction(SodaObject):
    def __init__(self, name, arity, compiler, package, line, col):
        self.name = name
        self.arity = arity
        self.compiler = compiler
        self.constbuffer = []
        self.package = package
        self.line = line
        self.col = col

    def evaluate_args(self, argstack):
        argstack.reverse()
        for i in range(0, len(self.compiler.constants)):
            self.constbuffer.append(self.compiler.constants[i])
            if isinstance(self.compiler.constants[i], SodaDummy):
                self.compiler.constants[i] = argstack.pop()

    def revert_state(self):
        self.compiler.constants = self.constbuffer
        self.constbuffer = []
