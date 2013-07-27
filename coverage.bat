@ECHO OFF
set PYTHONPATH=%CD%
set NOSE_WITH_COVERAGE=true
set NOSE_COVER_PACKAGE=ezodf
set NOSE=C:\Python33\Scripts\nosetests-script.py

py -3.3 %NOSE% %* 

set NOSE_WITH_COVERAGE=
