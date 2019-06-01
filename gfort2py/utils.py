# SPDX-License-Identifier: GPL-2.0+
from __future__ import print_function
import ctypes
import struct

def find_key_val(list_dicts, key, value):
    v = value.lower()
    for idx, i in enumerate(list_dicts):
        if i[key].lower() == v:
            return idx

_dictCTypes = {
        ('int',1): ctypes.c_int8,
        ('int',2): ctypes.c_int16,
        ('int',4): ctypes.c_int32,
        ('int',8): ctypes.c_int64,

        ('unsigned int',1): ctypes.c_uint8,
        ('unsigned int',2): ctypes.c_uint16,
        ('unsigned int',4): ctypes.c_uint32,
        ('unsigned int',8): ctypes.c_uint64,

        ('float',4): ctypes.c_float,
        
        ('float',8): ctypes.c_double,
        ('double',8): ctypes.c_double,
        ('quad',16): ctypes.c_longdouble,
        
        ('_Bool',1): ctypes.c_bool,
        ('char',1): ctypes.c_char,
        ('str',1): ctypes.c_char,
        }

_dictStTypes = {
        ('int',1): 'b',
        ('int',2): 'h',
        ('int',4): 'i',
        ('int',8): 'q',
        
        ('unsigned int',1): 'B',
        ('unsigned int',2): 'H',
        ('unsigned int',4): 'I',
        ('unsigned int',8): 'Q',

        ('float',4): 'f',
        
        ('float',8): 'd',
        ('double',8): 'd',
        
        ('_Bool',1): '?',
        ('char',1): 'c',
        }

_allStructsBase = {}

def makeCType(x,ptrs=True):
    res = None
    try:
        res = _dictCTypes[(x['pytype'],int(x['bytes']))]
    except TypeError:
        return None
    except KeyError:
        pass
        
    if 'length' in x:
        res = res * x['length']
    elif 'struct' in x and x['struct']:
        res = cstruct(_allStructsBase[x['pytype']])
    elif ptrs:
        res = ctypes.POINTER(res)

    return res
    
# def make_pointer_argtypes(value, cctype, nptrs=1):
    # res = value
    # if 'ptrs' in cctype and cctype['ptrs']>0:
        # if 'struct' in cctype and cctype['struct']:
            # res = ctypes.POINTER(value._bufferType)
            # nptrs = cctype['ptrs'] - 1
        # else:
            # nptrs = cctype['ptrs']
            # res = value
        
    # if nptrs > 0:
        # for i in range(nptrs):
            # res = ctypes.POINTER(res)  

    # return res

# def make_pointer_argsvalues(value, cctype, nptrs=1):
    # res = cctype
    # if 'ptrs' in cctype and cctype['ptrs']>0:
        # if 'struct' in cctype and cctype['struct']:
            # res = ctypes.pointer(value._ctype._buffer)
            # nptrs = cctype['ptrs'] - 1
        # else:
            # nptrs = cctype['ptrs']
            # res = value
        
    # if nptrs > 0:
        # for i in range(nptrs):
            # res = ctypes.POINTER(res)  

    # return res
