@ECHO OFF
SET PYTHONPATH=%CD%
SET PYTHON31=C:\Python31
SET PYEXE=%PYTHON31%\python.exe 
SET PYTEST=%PYTHON31%\Scripts\py.test-3.1-script.py

%PYEXE% %PYTEST% %*

