@set PYTHONPATH=%CD%
@set NOSE_WITH_COVERAGE=YES
@set NOSE_COVER_PACKAGE=ezodf

@C:\Python31\python.exe C:\Python31\Scripts\nosetests-script.py %*

@set NOSE_WITH_COVERAGE=
