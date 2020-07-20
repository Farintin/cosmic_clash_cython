import sys
import setup
import glob


if '--all' in sys.argv:
    sys.argv.remove('--all')
if len(sys.argv) == 3:
    sys.argv += glob.glob('*.pyx')

setup.build(sys.argv)
setup.start()