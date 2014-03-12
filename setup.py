# from distutils.core import setup
# from Cython.Build import cythonize

# setup(
#     name = 'LandBOS',
#     # ext_modules = cythonize('src/pybos.pyx')
#     ext_modules = cythonize('yo', ['landbos.pyx'])
# )


from distutils.core import setup
from distutils.extension import Extension

try:
    USE_CYTHON = True
    from Cython.Build import cythonize
except Exception:
    USE_CYTHON = False


ext = '.pyx' if USE_CYTHON else '.c'

extensions = [Extension('_landbos', ['src/_landbos'+ext, 'src/LandBOS.c'])]

if USE_CYTHON:
    extensions = cythonize(extensions)

setup(
    name = 'LandBOS',
    ext_modules = extensions
)