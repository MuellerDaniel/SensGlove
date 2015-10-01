# compile the code in terminal with
# $python setupCyPy.py build_ext --inplace

# then open a python interpreter and "import "spamTest.py""
# the functions get called automatically (because in "spamTest.py" you call them)
# when you want to call them by hand, just type "fcn.funcCy()"...

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
