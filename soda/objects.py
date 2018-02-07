from rply.token import BaseBox
from rpython.rlib.rstring import UnicodeBuilder
from math import fmod, pow

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
        assert isinstance(value, float)
        self.value = value

    def add(self, other):
        assert isinstance(other, SodaNumber)
        return SodaNumber(self.value + other.value)
    
    def sub(self, other):
        assert isinstance(other, SodaNumber)
        return SodaNumber(self.value - other.value)

    def mul(self, other):
        assert isinstance(other, SodaNumber)
        return SodaNumber(self.value * other.value)

    def div(self, other):
        assert isinstance(other, SodaNumber)
        return SodaNumber(self.value / other.value)

    def mod(self, other):
        assert isinstance(other, SodaNumber)
        return SodaNumber(fmod(self.value, other.value))

    def pow(self, other):
        assert isinstance(other, SodaNumber)
        return SodaNumber(pow(self.value, other.value))
    
    def str(self):
        s = "%f" % self.value
        if "." in s:
            s = s.rstrip("0").rstrip(".")
        return unicode(s).encode("utf-8")
