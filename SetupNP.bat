@echo off
:: SetupNP.bat - Copy the Docsfox program file into a Notepad++ folder
:: Copy docsfoxNP.py to C:\Users\%username%\AppData\Roaming\Notepad++\plugins\config\PythonScript\scripts
:: If this Setup file fails to run, you many need to:
::    Right-click it in Windows File Explorer.
::    Check the box: Unblock
:: -------------------------------------------
setlocal

set "CODEFILE=docsfoxNP.py"
if exist "%~dp0\%CODEFILE%" (
    echo .
) else (
    echo .   docsfoxNP.py needs to be copied from the 
    echo .   Docsfox ZIP into the same place as SetupNP.bat
    pause
    exit
)

set "TARGET_DIR=%APPDATA%\Notepad++\plugins\config\PythonScript\scripts"

if exist "%TARGET_DIR%\" (
    echo .
) else (
    echo .   Notepad++ is not installed.
    echo .   Please install Notepad++ and try again.
    pause
    exit
)
echo .
echo .
echo .   This setup program copies the
echo .   the Docsfox code file, docsfoxNP.py,
echo .   for use with Notepad++ Writer.
echo .
echo .   To quit, close this window, or
pause
cls
C:
md %TARGET_DIR%\Scripts
md %TARGET_DIR%\Scripts\python
copy %~dp0\docsfoxNP.py %TARGET_DIR%\
if exist "%TARGET_DIR%\Scripts\python\docsfoxNP.py" (
    echo .
    echo .
    echo .   SUCCESS!
) else (
    echo .
    echo .   This setup did not complete.
)
echo .
echo .
echo .
pause