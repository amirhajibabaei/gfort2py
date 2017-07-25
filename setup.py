#!/usr/bin/env python

import os
from setuptools import setup, find_packages

from distutils.core import setup, Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

import numpy as np
import os
import sysconfig

try:
	import unittest as unittest
except ImportError:
	import unittest2 as unittest


PY_INCLUDE = sysconfig.get_paths()['include']

SRC_DIR = "gfort2py"

ext = Extension(os.path.join(SRC_DIR,"fnumpy"),
				[os.path.join(SRC_DIR,"fnumpy.pyx")],
				include_dirs=[np.get_include(),PY_INCLUDE])

def my_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='*_test.py')
    return test_suite

setup(name='gfort2py',
      version='0.0',
      description='Python bindings for Fortran',
      license="GPLv2+",
      author='Robert Farmer',
      author_email='rjfarmer@asu.edu',
      url='https://github.com/rjfarmer/gfort2py',
      packages=["gfort2py"],
      classifiers=[
			"Development Status :: 1 - Planning",
			"License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
			"Programming Language :: Fortran",
      ],
      test_suite = 'tests',
	  cmdclass={"build_ext": build_ext},
	  ext_modules=cythonize(ext)
     )
