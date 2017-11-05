@echo off
cls
@echo ********************************************************************************
@echo Launch pre-procesador of code c/c++ 
@echo    python.exe build.by
@echo ********************************************************************************
call %PYTHON27%\python.exe PreProcessCode_C_CPP.py zfmem.c zfmem_.c
pause