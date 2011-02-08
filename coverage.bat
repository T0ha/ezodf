@ECHO OFF
set PYTHONPATH=%CD%
set NOSE_WITH_COVERAGE=true
set NOSE_COVER_PACKAGE=ezodf
set PYEXE=C:\Python31\python.exe
set NOSE=C:\Python31\Scripts\nosetests-script.py

%PYEXE% %NOSE% %* 

set NOSE_WITH_COVERAGE=
