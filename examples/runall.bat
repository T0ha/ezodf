@echo off
set PYTHON=c:\python31\python.exe
cd ..
set PYTHONPATH=%CD%
cd examples
for %%e in (*.py) do %PYTHON% %%e
