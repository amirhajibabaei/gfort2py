# SPDX-License-Identifier: GPL-2.0+
from __future__ import print_function
try:
    import __builtin__
except ImportError:
    import builtins as __builtin__

import ctypes
import numpy as np
from .errors import *
from .utils import *

# Hacky, yes
__builtin__.quad = np.longdouble

class fVar(object):
    def __init__(self, lib, var,const=False, name = None):
        self.lib = lib
        self.obj = var
        if 'var' in var:
            self.var = var['var']
        elif 'param' in var:
            self.var = var['param']
        self._ctype = makeCType(self.var,False)
        self.name = name
        self.const = const
        self._init = True

        if self.name is not None:
            self.in_dll()

    def from_param(self,obj):
        return self._ctype.from_param(obj)

    def from_address(self, address):
        return self._ctype.from_address(address)

    def from_buffer(self, source, offset=0):
        return self._ctype.from_buffer(source, offset)

    def from_buffer_copy(self, source, offset=0):
        return self._ctype.from_buffer_copy(source, offset)

    def in_dll(self):
        if self.const:
            self._ctype(self.value)
        else:
            return self._ctype.in_dll(self.lib, self.obj['mangled_name'])

    @property
    def value(self):
        if self.const:
            return self.var['value']
        
        x = self.in_dll()
        if x is None:
            return None

        if hasattr(x,'value'):
            return x.value
        else:
            while True:
                try:
                    x = x.contents
                except AttributeError:
                    break
            if hasattr(x,'value'):
                return x.value
            else:
                return x


    def set(self, value):
        if self.const:
            raise AttributeError('Can not set const variable')
        else:
            if hasattr(self._ctype,'contents'):
                self._ctype(value)
            else:
                try:
                    self.in_dll().value = value.encode()
                except (TypeError, AttributeError):
                    self.in_dll().value = value

    @property
    def _as_parameter_(self):
        return self._ctype._as_parameter_


    def __getitem__(self, key):
        if self.var['struct']:
            return self._ctype[key]
        else:
            raise TypeError('Not subscriptable')

    def __setitem__(self, key, value):
        if self.var['struct']:
            self._ctype[key] = value
        else:
            raise TypeError('Not subscriptable')

    def __contains__(self, key):
        if self.var['struct']:
            return key in self._ctype
        else:
            raise TypeError('Not subscriptable')

    def __dir__(self):
        if self.var['struct']:
            return self._ctype.keys()

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return str(self.value)

    def __add__(self, other):
        return getattr(self.value, '__add__')(other)

    def __sub__(self, other):
        return getattr(self.value, '__sub__')(other)

    def __mul__(self, other):
        return getattr(self.value, '__mul__')(other)

    def __matmul__(self,other):
        return getattr(self.value, '__matmul__')(other)

    def __truediv__(self, other):
        return getattr(self.value, '__truediv__')(other)
        
    def __floordiv__(self,other):
        return getattr(self.value, '__floordiv__')(other)

    def __pow__(self, other, modulo=None):
        return getattr(self.value, '__pow__')(other,modulo)

    def __mod__(self,other):
        return getattr(self.value, '__mod__')(other)        
        
    def __lshift__(self,other):
        return getattr(self.value, '__lshift__')(other)        

    def __rshift__(self,other):
        return getattr(self.value, '__rshift__')(other)

    def __and__(self,other):
        return getattr(self.value, '__and__')(other)
        
    def __xor__(self,other):
        return getattr(self.value, '__xor__')(other)
        
    def __or__(self,other):
        return getattr(self.value, '__or__')(other)
        
    def __radd__(self, other):
        return getattr(self.value, '__radd__')(other)

    def __rsub__(self, other):
        return getattr(self.value, '__rsub__')(other)

    def __rmul__(self, other):
        return getattr(self.value, '__rmul__')(other)

    def __rmatmul__(self,other):
        return getattr(self.value, '__rmatmul__')(other)

    def __rtruediv__(self, other):
        return getattr(self.value, '__rtruediv__')(other)
        
    def __rfloordiv__(self,other):
        return getattr(self.value, '__rfloordiv__')(other)

    def __rpow__(self, other):
        return getattr(self.value, '__rpow__')(other)

    def __rmod__(self,other):
        return getattr(self.value, '__rmod__')(other)        
        
    def __rlshift__(self,other):
        return getattr(self.value, '__rlshift__')(other)        

    def __rrshift__(self,other):
        return getattr(self.value, '__rrshift__')(other)

    def __rand__(self,other):
        return getattr(self.value, '__rand__')(other)
        
    def __rxor__(self,other):
        return getattr(self.value, '__rxor__')(other)
        
    def __ror__(self,other):
        return getattr(self.value, '__ror__')(other)

    def __iadd__(self, other):
        self.set(self.value + other)
        return self.value

    def __isub__(self, other):
        self.set(self.value - other)
        return self.value

    def __imul__(self, other):
        self.set(self.value * other)
        return self.value

    def __itruediv__(self, other):
        self.set(self.value / other)
        return self.value

    def __ipow__(self, other, modulo=None):
        x = self.value**other
        if modulo:
            x = x % modulo
        self.set(x)
        return self.value

    def __eq__(self, other):
        return self.value == other

    def __neq__(self, other):
        return self.value != other

    def __lt__(self, other):
        return getattr(self.value, '__lt__')(other)

    def __le__(self, other):
        return getattr(self.value, '__le__')(other)

    def __gt__(self, other):
        return getattr(self.value, '__gt__')(other)

    def __ge__(self, other):
        return getattr(self.value, '__ge__')(other)
        
    def __format__(self, other):
        return getattr(self.value, '__format__')(other)
  
    def __bytes__(self):
        return getattr(self.value, '__bytes__')()  
        
    def __bool__(self):
        return getattr(self.value, '__bool__')()
   
    def __len__(self):
        return getattr(self.value, '__len__')()


# class fVar(object):

    # def __init__(self, lib, obj, name=None):
        # self.__dict__.update(obj)
        # self._lib = lib
        # self.ctype=self.var['ctype']
        # self.pytype=self.var['pytype']
        
        # self._pytype = self.pytype_def()
        # if self.pytype == 'quad':
            # self.pytype = np.longdouble
        # elif self.pytype=='bool':
            # self.pytype=int
            # self.ctype='c_int32'
        
        # self._ctype = self.ctype_def()
        # #self._ctype_f = self.ctype_def_func()

        # # if true for things that are fortran things
        # self._fortran = True
        
        # # True if its a function argument
        # self._func_arg = False
        
        # #True if struct member
        # self._dt_arg = False
        
        # #Store the ref to the lib object
        # try:   
            # self._ref = self._get_from_lib()
        # except NotInLib:
            # self._ref = None
            
            

        # self.lib = lib
        # self.obj = obj
        # self.var = var['def']
        # self._ctype = makeCType(self.var)
        # self.name = name
        # self._init = True

        # if self.name is not None:
            # self.in_dll()

    # def from_param(self,obj):
        # return self._ctype.from_param(obj)

    # def from_address(self, address):
        # return self._ctype.from_address(address)

    # def from_buffer(self, source, offset=0):
        # return self._ctype.from_buffer(source, offset)

    # def from_buffer_copy(self, source, offset=0):
        # return self._ctype.from_buffer_copy(source, offset)

    # def in_dll(self):
        # return self._ctype.in_dll(self.lib, self.name)

    # @property
    # def value(self):
        # x = self._ctype.in_dll(self.lib, self.name)
        # if x is None:
            # return None

        # if hasattr(x,'value'):
            # return x.value
        # else:
            # while True:
                # try:
                    # x = x.contents
                # except AttributeError:
                    # break
            # if hasattr(x,'value'):
                # return x.value
            # else:
                # return x


    # def set(self, value):
        # if self.var['const']:
            # raise AttributeError('Can not set const variable')
        # else:
            # if hasattr(self._ctype,'contents'):
                # self._ctype(value)
            # else:
                # self.in_dll().value = value

    # @property
    # def _as_parameter_(self):
        # return self._ctype._as_parameter_


    # def __getitem__(self, key):
        # if self.var['struct']:
            # return self._ctype[key]
        # else:
            # raise TypeError('Not subscriptable')

    # def __setitem__(self, key, value):
        # if self.var['struct']:
            # self._ctype[key] = value
        # else:
            # raise TypeError('Not subscriptable')

    # def __contains__(self, key):
        # if self.var['struct']:
            # return key in self._ctype
        # else:
            # raise TypeError('Not subscriptable')

    # def __dir__(self):
        # if self.var['struct']:
            # return self._ctype.keys()

    # def __repr__(self):
        # return str(self.value)

    # def __str__(self):
        # return str(self.value)

    # def __add__(self, other):
        # return getattr(self.value, '__add__')(other)

    # def __sub__(self, other):
        # return getattr(self.value, '__sub__')(other)

    # def __mul__(self, other):
        # return getattr(self.value, '__mul__')(other)

    # def __matmul__(self,other):
        # return getattr(self.value, '__matmul__')(other)

    # def __truediv__(self, other):
        # return getattr(self.value, '__truediv__')(other)
        
    # def __floordiv__(self,other):
        # return getattr(self.value, '__floordiv__')(other)

    # def __pow__(self, other, modulo=None):
        # return getattr(self.value, '__pow__')(other,modulo)

    # def __mod__(self,other):
        # return getattr(self.value, '__mod__')(other)        
        
    # def __lshift__(self,other):
        # return getattr(self.value, '__lshift__')(other)        

    # def __rshift__(self,other):
        # return getattr(self.value, '__rshift__')(other)

    # def __and__(self,other):
        # return getattr(self.value, '__and__')(other)
        
    # def __xor__(self,other):
        # return getattr(self.value, '__xor__')(other)
        
    # def __or__(self,other):
        # return getattr(self.value, '__or__')(other)
        
    # def __radd__(self, other):
        # return getattr(self.value, '__radd__')(other)

    # def __rsub__(self, other):
        # return getattr(self.value, '__rsub__')(other)

    # def __rmul__(self, other):
        # return getattr(self.value, '__rmul__')(other)

    # def __rmatmul__(self,other):
        # return getattr(self.value, '__rmatmul__')(other)

    # def __rtruediv__(self, other):
        # return getattr(self.value, '__rtruediv__')(other)
        
    # def __rfloordiv__(self,other):
        # return getattr(self.value, '__rfloordiv__')(other)

    # def __rpow__(self, other):
        # return getattr(self.value, '__rpow__')(other)

    # def __rmod__(self,other):
        # return getattr(self.value, '__rmod__')(other)        
        
    # def __rlshift__(self,other):
        # return getattr(self.value, '__rlshift__')(other)        

    # def __rrshift__(self,other):
        # return getattr(self.value, '__rrshift__')(other)

    # def __rand__(self,other):
        # return getattr(self.value, '__rand__')(other)
        
    # def __rxor__(self,other):
        # return getattr(self.value, '__rxor__')(other)
        
    # def __ror__(self,other):
        # return getattr(self.value, '__ror__')(other)

    # def __iadd__(self, other):
        # self.set(self.value + other)
        # return self.value

    # def __isub__(self, other):
        # self.set(self.value - other)
        # return self.value

    # def __imul__(self, other):
        # self.set(self.value * other)
        # return self.value

    # def __itruediv__(self, other):
        # self.set(self.value / other)
        # return self.value

    # def __ipow__(self, other, modulo=None):
        # x = self.value**other
        # if modulo:
            # x = x % modulo
        # self.set(x)
        # return self.value

    # def __eq__(self, other):
        # return self.value == other

    # def __neq__(self, other):
        # return self.value != other

    # def __lt__(self, other):
        # return getattr(self.value, '__lt__')(other)

    # def __le__(self, other):
        # return getattr(self.value, '__le__')(other)

    # def __gt__(self, other):
        # return getattr(self.value, '__gt__')(other)

    # def __ge__(self, other):
        # return getattr(self.value, '__ge__')(other)
        
    # def __format__(self, other):
        # return getattr(self.value, '__format__')(other)
  
    # def __bytes__(self):
        # return getattr(self.value, '__bytes__')()  
        
    # def __bool__(self):
        # return getattr(self.value, '__bool__')()
   
    # def __len__(self):
        # return getattr(self.value, '__len__')()
