# Phillip Wells
# CSCI-200 Algorithm Analysis

# objects.py defines the primitive datatypes of soda

from rply.token import BaseBox
from rpython.rlib.rstring import replace, UnicodeBuilder
from rpython.rlib.rbigint import rbigint


class SodaObject(BaseBox):
    pass


class SodaDummy(SodaObject):
    def __init__(self):
        pass


class SodaBuilder(SodaObject):
    def __init__(self, value):
        self.value = value

    def concat(self, other):
        self.value.append(unicode(other.str()))
        return SodaBuilder(self.value)

    def diff(self, other):
        return (self.tostr().diff(other.tostr()))

    def getkey(self, keypos):
        raise Exception

    def setval(self, idx, value):
        raise Exception

    def getval(self, idx):
        string = self.value.build()
        if idx.toint().integer() > len(string) - 1:
            raise IndexError
        val = string[idx.toint().integer()]
        return SodaString(val)

    def eq(self, other):
        return (self.tostr().eq(other.tostr()))

    def ne(self, other):
        return (self.tostr().ne(other.tostr()))

    def gt(self, other):
        return (self.tostr().gt(other.tostr()))

    def lt(self, other):
        return (self.tostr().lt(other.tostr()))

    def ge(self, other):
        return (self.tostr().ge(other.tostr()))

    def le(self, other):
        return (self.tostr().le(other.tostr()))

    def land(self, other):
        return (self.tostr().land(other.tostr()))

    def lor(self, other):
        return (self.tostr().lor(other.tostr()))

    def lnot(self):
        return (self.tostr().lnot())

    def isstr(self):
        return True

    def isint(self):
        return False

    def isarray(self):
        return False

    def toint(self):
        a = rbigint()
        number = a.fromstr(str(self.value.build()))
        return SodaInt(number)

    def tostr(self):
        return SodaString(self.value.build())

    def str(self):
        return self.value.build().encode("utf-8")


class SodaString(SodaObject):
    def __init__(self, value):
        assert isinstance(value, unicode)
        self.value = value
        a = rbigint()
        self.length = SodaInt(a.fromint(len(self.value)))

    def concat(self, other):
        builder = UnicodeBuilder()
        builder.append(self.value)
        builder.append(unicode(other.str()))
        return SodaBuilder(builder)

    def diff(self, other):
        assert isinstance(other, SodaString)
        return SodaString(replace(self.value, other.value, u""))

    def getkey(self, keypos):
        raise Exception

    def getval(self, idx):
        if idx.toint().integer() > len(self.value) - 1:
            raise IndexError
        val = self.value[idx.toint().integer()]
        return SodaString(val)

    def setval(self, idx, value):
        raise Exception

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
        if not (self.value == u"false" or other.value == u"false"):
            return SodaString(u"true")
        else:
            return SodaString(u"false")

    def lor(self, other):
        assert isinstance(other, SodaString)
        if not (self.value == u"false" and other.value == u"false"):
            return SodaString(u"true")
        else:
            return SodaString(u"false")

    def lnot(self):
        if not self.value == u"false":
            return SodaString(u"false")
        else:
            return SodaString(u"true")

    def isstr(self):
        return True

    def isint(self):
        return False

    def isarray(self):
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
        self.length = None

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

    def isarray(self):
        return False

    def toint(self):
        return SodaInt(self.value)

    def integer(self):
        return self.value.toint()

    def getkey(self, keypos):
        raise Exception

    def getval(self, idx):
        raise Exception

    def setval(self, idx, value):
        raise Exception

    def tostr(self):
        return SodaString(self.str().decode("utf-8"))

    def str(self):
        s = self.value.str()
        return unicode(s).encode("utf-8")


class SodaArray(SodaObject):
    def __init__(self, itemlist):
        self.value = {}
        self.keys = []
        i = 0
        while i < len(itemlist):
            self.value[itemlist[i].str()] = itemlist[i + 1]
            self.keys.append(itemlist[i])
            i += 2
        a = rbigint()
        self.length = SodaInt(a.fromint(len(self.value)))

    def getkey(self, keypos):
        if keypos < len(self.keys):
            key = self.keys[keypos]
        else:
            key = None
        return key

    def getval(self, idx):
        try:
            return self.value[idx.str()]
        except KeyError:
            return SodaString(u"")

    def setval(self, idx, value):
        self.value[idx.str()] = value
        self.keys.append(idx)
        a = rbigint()
        self.length = SodaInt(a.fromint(len(self.value)))

    def isstr(self):
        return False

    def isint(self):
        return False

    def isarray(self):
        return True

    def toint(self):
        raise Exception

    def tostr(self):
        raise Exception

    def str(self):
        s = []
        for key in self.value:
            val = self.value[key]
            s.append("\"" + key + "\" : "
                     "\"" + val.str() + "\"")
        return unicode("[" + ", ".join(s) +
                       "]").encode("utf-8")


class SodaFunction(SodaObject):
    def __init__(self, name, arity, compiler, package, line, col):
        self.name = name
        self.arity = arity
        self.numargs = arity
        self.isvariadic = False
        self.compiler = compiler
        self.constbuffer = []
        self.package = package
        self.line = line
        self.col = col

    def evaluate_args(self, argstack):
        argstack.reverse()
        if self.isvariadic:
            a = rbigint()
            enumlist = []
            nargstack = []
            j = 0
            for i in range(self.arity - 1, len(argstack)):
                enumlist.append(SodaInt(a.fromint(j)))
                enumlist.append(argstack[i])
                j += 1
            for k in range(0, self.arity - 1):
                nargstack.append(argstack[k])
            argstack = nargstack
            argstack.append(SodaArray(enumlist))
        for i in range(0, len(self.compiler.constants)):
            self.constbuffer.append(self.compiler.constants[i])
            if isinstance(self.compiler.constants[i], SodaDummy):
                self.compiler.constants[i] = argstack.pop()

    def revert_state(self):
        self.compiler.constants = self.constbuffer
        self.constbuffer = []
