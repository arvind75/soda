from rply.token import BaseBox
from rpython.rlib.rbigint import rbigint


class SodaObject(BaseBox):
    pass


class SodaString(SodaObject):
    def __init__(self, value):
        assert isinstance(value, unicode)
        self.value = value

    def eq(self, other):
        assert isinstance(other, SodaString)
        if (self.value == other.value):
            return SodaString(u"true")
        else:
            return SodaString(u"false")

    def neq(self, other):
        assert isinstance(other, SodaString)
        if (self.value != other.value):
            return SodaString(u"true")
        else:
            return SodaString(u"false")

    def gre(self, other):
        assert isinstance(other, SodaString)
        if (self.value > other.value):
            return SodaString(u"true")
        else:
            return SodaString(u"false")

    def les(self, other):
        assert isinstance(other, SodaString)
        if (self.value < other.value):
            return SodaString(u"true")
        else:
            return SodaString(u"false")

    def geq(self, other):
        assert isinstance(other, SodaString)
        if (self.value >= other.value):
            return SodaString(u"true")
        else:
            return SodaString(u"false")

    def leq(self, other):
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

    def str(self):
        return self.value.encode("utf-8")


class SodaNumber(SodaObject):
    def __init__(self, value):
        assert isinstance(value, rbigint)
        self.value = value

    def add(self, other):
        assert isinstance(other, SodaNumber)
        return SodaNumber(self.value.add(other.value))

    def sub(self, other):
        assert isinstance(other, SodaNumber)
        return SodaNumber(self.value.sub(other.value))

    def mul(self, other):
        assert isinstance(other, SodaNumber)
        return SodaNumber(self.value.mul(other.value))

    def div(self, other):
        assert isinstance(other, SodaNumber)
        return SodaNumber(self.value.floordiv(other.value))

    def mod(self, other):
        assert isinstance(other, SodaNumber)
        return SodaNumber(self.value.mod(other.value))

    def pow(self, other):
        assert isinstance(other, SodaNumber)
        return SodaNumber(self.value.pow(other.value))

    def eq(self, other):
        assert isinstance(other, SodaNumber)
        if (self.value.eq(other.value)):
            return SodaString(u"true")
        else:
            return SodaString(u"false")

    def neq(self, other):
        assert isinstance(other, SodaNumber)
        if (self.value.ne(other.value)):
            return SodaString(u"true")
        else:
            return SodaString(u"false")

    def gre(self, other):
        assert isinstance(other, SodaNumber)
        if (self.value.gt(other.value)):
            return SodaString(u"true")
        else:
            return SodaString(u"false")

    def les(self, other):
        assert isinstance(other, SodaNumber)
        if (self.value.lt(other.value)):
            return SodaString(u"true")
        else:
            return SodaString(u"false")

    def geq(self, other):
        assert isinstance(other, SodaNumber)
        if (self.value.ge(other.value)):
            return SodaString(u"true")
        else:
            return SodaString(u"false")

    def leq(self, other):
        assert isinstance(other, SodaNumber)
        if (self.value.le(other.value)):
            return SodaString(u"true")
        else:
            return SodaString(u"false")

    def str(self):
        s = self.value.str()
        return unicode(s).encode("utf-8")
