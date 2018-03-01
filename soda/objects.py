from rply.token import BaseBox
from rpython.rlib.rbigint import rbigint


class SodaObject(BaseBox):
    pass


class SodaString(SodaObject):
    def __init__(self, value):
        assert isinstance(value, unicode)
        self.value = value

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

    def str(self):
        s = self.value.str()
        return unicode(s).encode("utf-8")
