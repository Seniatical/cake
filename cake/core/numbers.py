from __future__ import annotations
from cake import (
    INumber,
    IComplex,
    IReal,
    IRational,
    IIntegeral,
    IVariable
)
import numbers
from math import trunc, floor, ceil
from cake import BasicExpression, Expression
from cake.basic import OtherType

from typing import Any, Union, Tuple
# Other type may be a basic expr, a cake library number or a generic python number

''' Methods implemented
__add__, __radd__, __iadd__
__sub__, __rsub__, __isub__
__mul__, __rmul__, __imul__
__truediv__, __rtruediv__, __itruediv__
__floordiv__, __rfloordiv__, __ifloordiv__
__mod__, __rmod__, __imod__
__divmod__, __rdivmod__
__pow__, __rpow__, __ipow__
__lshift__, __rlshift__, __ilshift__
__rshift__, __rrshift__, __irshift__
__and__, __rand__, __iand__
__xor__, __rxor__, __ixor__
__or__, __ror__, __ior__
__neg__, __pos__, __abs__, __invert__
__complex__, __float__, __int__, __str__, __bool__
__format__
__eq__, __ne__, __lt__, __gt__, __le__, __ge__
__call__, __round__, __trunc__, __floor__, __ceil__
'''
class Number(INumber):
    ''' Basic class for creating different types of numbers, 
        this class can be treated as a normal integer.

    .. code-block:: py

        from cake import Number, Variable
        
        x = 5
        x += Number(10)
        ## x is now an Integral not a Number

        a = Variable('a')
        x = x + a
        ## x is now an Expression
        ## x = Expr(Integral(15), Variable('a'))
        ## which can be represented as f(x) = 15 + a
    '''
    _type = None

    def __init_subclass__(cls, type, *args, **kwds) -> None:
        cls._type = type

        return super().__init_subclass__(*args, **kwds)

    @staticmethod
    def convert(x: Union[Number, numbers.Number, BasicExpression]) -> Number:
        ## Helper method for converting between number types on results
        if isinstance(x, BasicExpression):
            return x

        if isinstance(x, int):
            return Integral(x)
        elif isinstance(x, float):
            return Real(x)
        elif isinstance(x, complex):
            return Complex(x)
        return x

    def to_expr(self, *leading_nodes) -> Expression:
        return Expression(self, *leading_nodes)

    def __add__(self, other: OtherType) -> OtherType:
        if isinstance(other, BasicExpression):
            other += self
            return other

        if isinstance(other, NumInstance):
            return self.convert(self.value + getattr(other, 'value', other))

        return Expression(self, other)

    __radd__ = __add__
    __iadd__ = __add__

    def __sub__(self, other: OtherType) -> OtherType:
        return self.__add__(-other)

    def __rsub__(self, other: OtherType) -> OtherType:
        x = -self
        if isinstance(other, BasicExpression):
            other += x
            return other

        if isinstance(other, NumInstance):
            return self.convert(other.value + x)
        
        return Expression(other, x)

    __isub__ = __sub__

    def __mul__(self, other: OtherType) -> OtherType:
        r = other * self.value
        if isinstance(r, NumInstance):
            return self.convert(r)
        return r

    __rmul__ = __mul__
    __imul__ = __mul__

    def __truediv__(self, other: OtherType) -> OtherType:
        r = self.value / other
        if isinstance(r, NumInstance):
            return self.convert(r)
        return r
    
    def __rtruediv__(self, other: OtherType) -> OtherType:
        r = other / self.value
        if isinstance(r, NumInstance):
            return self.convert(r)
        return r

    __itruediv__ = __truediv__

    def __floordiv__(self, other: OtherType) -> OtherType:
        r = self.value // other
        if isinstance(r, NumInstance):
            return self.convert(r)
        return r
    
    def __rfloordiv__(self, other: OtherType) -> OtherType:
        r = other // self.value
        if isinstance(r, NumInstance):
            return self.convert(r)
        return r

    __ifloordiv__ = __floordiv__

    def __mod__(self, other: OtherType) -> OtherType:
        r = self.value % other
        if isinstance(r, NumInstance):
            return self.convert(r)
        return r

    def __rmod__(self, other: OtherType) -> OtherType:
        r = other % self.value
        if isinstance(r, NumInstance):
            return self.convert(r)
        return r

    __imod__ = __mod__

    def __divmod__(self, other: OtherType) -> Tuple[OtherType, OtherType]:
        truediv = self.__floordiv__(other)
        mod = self.__mod__(other)

        return (truediv, mod)

    def __rdivmod__(self, other: OtherType) -> Tuple[OtherType, OtherType]:
        truediv = other.__floordiv__(self.value)
        mod = other.__mod__(self.value)

        return (self.convert(truediv), self.convert(mod))

    def __pow__(self, other: OtherType, *modulo: NumInstance) -> OtherType:
        r = self.value ** other
        if modulo:
            r %= modulo[0]

        if isinstance(r, NumInstance):
            return self.convert(r)
        return r

    def __rpow__(self, other: OtherType, *modulo: NumInstance) -> OtherType:
        r = other ** self.value
        if modulo:
            r %= modulo[0]

        if isinstance(r, NumInstance):
            return self.convert(r)
        return r

    __ipow__ = __pow__

    def __lshift__(self, other: OtherType) -> OtherType:
        r = self.value << other
        if isinstance(r, NumInstance):
            return self.convert(r)
        return r

    def __rshift__(self, other: OtherType) -> OtherType:
        r = self.value >> other
        if isinstance(r, NumInstance):
            return self.convert(r)
        return r

    __ilshift__ = __lshift__
    __irshift__ = __rshift__

    def __rlshift__(self, other: OtherType) -> OtherType:
        r = other << self.value
        if isinstance(r, NumInstance):
            return self.convert(r)
        return r

    def __rrshift__(self, other: OtherType) -> OtherType:
        r = other >> self.value
        if isinstance(r, NumInstance):
            return self.convert(r)
        return r

    def __and__(self, other: OtherType) -> OtherType:
        r = self.value & other
        if isinstance(r, NumInstance):
            return self.convert(r)
        return r

    def __rand__(self, other: OtherType) -> OtherType:
        r = self.value & other
        if isinstance(r, NumInstance):
            return self.convert(r)
        return r

    __iand__ = __and__

    def __xor__(self, other: OtherType) -> OtherType:
        r = self.value ^ other
        if isinstance(r, NumInstance):
            return self.convert(r)
        return r

    def __rxor__(self, other: OtherType) -> OtherType:
        r = self.value ^ other
        if isinstance(r, NumInstance):
            return self.convert(r)
        return r

    __ixor__ = __xor__

    def __or__(self, other: OtherType) -> OtherType:
        r = self.value | other
        if isinstance(r, NumInstance):
            return self.convert(r)
        return r

    def __ror__(self, other: OtherType) -> OtherType:
        r = self.value | other
        if isinstance(r, NumInstance):
            return self.convert(r)
        return r

    __ior__ = __or__

    def __neg__(self) -> Number:
        return self.convert(-self.value)

    def __pos__(self) -> Number:
        return self

    def __abs__(self) -> Number:
        if self.value < 0:
            return self.__neg__()
        return self

    def __invert__(self) -> Number:
        return self.convert(~self.value)

    ''' END NUMERICAL METHODS '''

    def __complex__(self) -> Complex:
        return complex(self.value)

    def __float__(self) -> Real:
        return float(self.value)

    def __int__(self) -> Integral:
        return int(self.value)

    def __str__(self) -> str:
        return str(self.value)

    def __bool__(self) -> bool:
        return self.value != 0

    def __format__(self, __format_spec: str) -> str:
        return self.value.__format__(__format_spec)

    ''' END CONVERSION METHODS '''

    def __eq__(self, other: OtherType) -> bool:
        return self.value == other

    def __ne__(self, other: OtherType) -> bool:
        return self.value != other
    
    def __lt__(self, other: OtherType) -> bool:
        return self.value < other
    
    def __gt__(self, other: OtherType) -> bool:
        return self.value > other

    def __le__(self, other: OtherType) -> bool:
        return self.value <= other

    def __ge__(self, other: OtherType) -> bool:
        return self.value >= other

    ''' END COMPARATIVE METHODS '''

    def __call__(self, other: OtherType) -> Any:
        ## Equivalent to __mul__, were 10 * 5 is represented as 10(5)
        return self.__mul__(other)

    def __round__(self, *ndigits: int) -> OtherType:
        return round(self.value, *ndigits)

    def __trunc__(self) -> OtherType:
        return trunc(self.value)

    def __floor__(self) -> OtherType:
        return floor(self.value)

    def __ceil__(self) -> OtherType:
        return ceil(self.value)

NumInstance = (Number, numbers.Number)


class Complex(Number, IComplex, numbers.Complex, type=complex):
    ...


class Real(Complex, IReal, numbers.Real, type=float):
    def as_integer_ratio(self):
        return self.value.as_integer_ratio()


class Rational(Real, IRational, numbers.Rational, type=float):
    ...


class Integral(Rational, IIntegeral, numbers.Integral, type=int):
    ...
