from distutils.core import setup
from Cython.Build import cythonize
import subprocess as sub



#setup(ext_modules = cythonize('gameCy.pyx'))
#setup(ext_modules = cythonize('celestCy.pyx'))
#setup(ext_modules = cythonize('craftsCy.pyx'))
#setup(ext_modules = cythonize('starsCy.pyx'))
def build(sys_argv):
    files = sys_argv[3:]
    del sys_argv[3:]
    import sys
    sys.argv = sys_argv
    for fl in files:
        if not '.' in fl:
            fl += '.pyx'
        setup(ext_modules = cythonize(fl))

def start():
    sub.call(['python', 'mainCy.py'])