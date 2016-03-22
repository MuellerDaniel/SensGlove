# compile the code in terminal with
# $python setupCylModel_A.py build_ext --inplace

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

ext_modules=[
    Extension("cylModel_A",
                sources=["cylModel_A.pyx"],
                libraries=["m"]
    )
]

setup(

    name = "CylModel_A",
    ext_modules = cythonize(ext_modules)
)
