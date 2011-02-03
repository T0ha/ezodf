#!c:\python31\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'pytest==2.0.0','console_scripts','py.test-3.1'
__requires__ = 'pytest==2.0.0'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('pytest==2.0.0', 'console_scripts', 'py.test-3.1')()
    )
