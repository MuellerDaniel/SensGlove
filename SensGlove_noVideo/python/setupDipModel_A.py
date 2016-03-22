# compile the code in terminal with
# $python setupDipModel_A.py build_ext --inplace

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

ext_modules=[
    Extension("dipModel_A",
                sources=["dipModel_A.pyx"],
                libraries=["m"]
    )
]

setup(

    name = "DipModel_A",
    ext_modules = cythonize(ext_modules)
)
