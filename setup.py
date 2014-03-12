from distutils.core import setup
from Cython.Build import cythonize

setup(
    name = 'LandBOS',
    # ext_modules = cythonize('src/pybos.pyx')
    ext_modules = cythonize('landbos.pyx')
)