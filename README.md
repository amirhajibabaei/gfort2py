![Build status](https://travis-ci.org/rjfarmer/gfort2py.svg?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/rjfarmer/gfort2py/badge.svg?branch=master)](https://coveralls.io/github/rjfarmer/gfort2py?branch=master)
[![PyPI version](https://badge.fury.io/py/gfort2py.svg)](https://badge.fury.io/py/gfort2py)
[![DOI](https://zenodo.org/badge/72889348.svg)](https://zenodo.org/badge/latestdoi/72889348)



# gfort2py
Library to allow calling fortran code from python. Requires gfortran>=5.3.1

Current stable version is 1.0.11

## Build
````bash
ipython3 setup.py install --user
````

or install via pip
````bash
pip install --user gfort2py
````

## Why use this over other fortran to python translators?

gfort2py use gfortran .mod files to translate your fortran code's ABI to python 
compatible types using python's ctype library. The advantage here is that it can
(in principle) handle anything the compiler can compile. gfort2py is almost entirely
python and there are no changes needed to your fortran source code (some changes in the build
process may be needed, as gfort2py needs your code compiled as a shared library). Disadvantage
means we are tied to gfortran and can't support other compilers and may break when
gfortran updates its .mod file format, though this happens rarely.


## Using
### Fortran side
Compile code with -fPIC and -shared as options, then link togethter as a shared lib at the end

````bash
gfortran -fPIC -shared -c file.f90
gfortran -fPIC -shared -o libfile file.f90
````
If your code comes as  program that does everything, then just turn the program into a function call inside a module,
then create a new file with your program that uses the module and calls the function you just made.

If the shared library needs other
shared libraries you will need to set LD_LIBRARY_PATH environment variable, and its also recommended is to run chrpath on the 
shared libraries so you can access them from anywhere.

### Python side
````python

import gfort2py as gf

SHARED_LIB_NAME='./test_mod.so'
MOD_FILE_NAME='tester.mod'

x=gf.fFort(SHARED_LIB_NAME,MOD_FILE_NAME)

````

x now contains all variables, parameters and functions from the module (tab completable). 

### Functions
````python
y = x.func_name(a,b,c)
````

Will call the fortran function with variables a,b,c and will return the result in y,
subroutines will return a dict (possibly empty) with any intent out, inout or undefined intent variables.

Optional arguments are handled by not passing anything for that item (python side), but
they must be at the end of the argument list (on the fortran side)

Array arguments must pass a numpy array, either pre filled (if the array is intent(in)) or made with zeros
if the array is intent out or allocatable.

### Variables

````python
x.some_var = 1
````

Sets a module variable to 1, will attempt to coerce it to the fortran type

````python
x.some_var
x.some_var.get()
````

First will print the value in some_var while get() will return the value

### Arrays

Remember that fortran by default has 1-based array numbering while numpy
is 0-based.


### Derived types

Derived types can be set with a dict 
````python
x.my_dt={'x':1,'y':'abc'}
````
And return a dict when the .get() method is called, unless you pass
copy=False to the get call in which case a ctype is returned (and fields
access via the dot interface)

````python
y=x.my_dt.get(copy=False)
y.x
y.y
````
If the derived type contains another derived type then you can set a dict in a dict

````python
x.my_dt={'x':1,'y':{'a':1}}
````

This can then be accessed either via:

````python
x.my_dt.y
````

To get a dict back, or:

````python
x.my_dt.y.a
x.my_dt['a']
````

To get a single value.

When setting the components of a derived type you do not need to specify
all of them at the same time.


## Testing

````bash
ipython3 setup.py test
````

To run unit tests

## Things that work

### Module variables

- [x] Scalars
- [x] Parameters
- [x] Characters
- [x] Explicit size arrays
- [X] Complex numbers (Scalar and parameters)
- [x] Getting a pointer
- [x] Getting the value of a pointer
- [x] Allocatable arrays
- [x] Derived types
- [x] Nested derived types
- [ ] Arrays of derived types
- [ ] Functions inside derived types
- [ ] Arrays with dimension (:) (pointer, allocatable) insider derived types (it doesn't break if their there, but you cant access them easily)
- [ ] Classes
- [ ] Abstract interfaces
- [ ] Common blocks
- [ ] Equivalences
- [ ] Namelists

### Functions/subroutines

- [X] Basic calling (no arguments)
- [x] Argument passing (scalars)
- [x] Argument passing (strings)
- [X] Argument passing (explicit arrays)
- [x] Argument passing (assumed size arrays)
- [x] Argument passing (assumed shape arrays)
- [x] Argument passing (allocatable arrays)
- [x] Argument passing (derived types)
- [x] Argument intents (in, out, inout and none)
- [x] Passing characters
- [x] Pointer Arguments 
- [x] Optional arguments
- [ ] Keyword arguments
- [ ] Generic/Elemental functions
- [ ] Functions as an argument

## Contributing

Pull requests should target the maint branch for fixing issues, please check the test suite
passes before sending a pull request.
Maint will be periodically merged with master for new releases, master should never have 
a broken test suite.
The dev branch is a longer term rewrite that is likely to be constantly broken.

