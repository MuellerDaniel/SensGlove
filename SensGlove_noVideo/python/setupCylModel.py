# compile the code in terminal with
# $python setupCylModel.py build_ext --inplace

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

ext_modules=[
    Extension("cylModel",
                sources=["cylModel.pyx"],
                libraries=["m"]
    )
]

setup(

    name = "CylModel",
    ext_modules = cythonize(ext_modules)
)
