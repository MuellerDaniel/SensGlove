# compile the code in terminal with
# $python setupDipModel.py build_ext --inplace

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

ext_modules=[
    Extension("dipModel",
                sources=["dipModel.pyx"],
                libraries=["m"]
    )
]

setup(

    name = "DipModel",
    ext_modules = cythonize(ext_modules)
)
