# compile the code in terminal with
# $python setupCyPy.py build_ext --inplace

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

ext_modules=[
    Extension("fcnCyPy",
                sources=["fcnCyPy.pyx"],
                libraries=["m"]
    )
]

setup(
    #ext_modules = cythonize("first.pyx")
    #ext_modules = cythonize("standalonecypy.pyx")

    name = "FcnCyPy",
    ext_modules = cythonize(ext_modules)
)
