@echo off
:: SetupLibre.bat - Create folders for the Docsfox code file for LibreOffice
:: Copy docsfoxLO.py to C:\Users\%username%\AppData\Roaming\LibreOffice\4\user\Scripts\python\
:: If this Setup file fails to run, you many need to:
::    Right-click it in Windows File Explorer.
::    Check the box: Unblock
:: ------------------------------------------
setlocal

set "CODEFILE=docsfoxLO.py"
if exist "%~dp0\%CODEFILE%" (
    echo .
) else (
    echo .   docsfoxLO.py needs to be copied from the 
    echo .   Docsfox ZIP into the same place as SetupLibre.bat
    pause
    exit
)

set "TARGET_DIR=%APPDATA%\LibreOffice\4\user"

if exist "%TARGET_DIR%\" (
    echo .
) else (
    echo .   LibreOffice is not installed.
    echo .   Please install LibreOffice and try again.
    pause
    exit
)
echo .
echo .
echo .   This setup program creates folders for
echo .   the Docsfox code file, docsfoxLO.py,
echo .   for use with LibreOffice Writer.
echo .
echo .   To quit, close this window, or
pause
cls
C:
md %TARGET_DIR%\Scripts
md %TARGET_DIR%\Scripts\python
copy %~dp0\docsfoxLO.py %TARGET_DIR%\Scripts\python\
if exist "%TARGET_DIR%\Scripts\python\docsfoxLO.py" (
    echo .
    echo .
    echo .   SUCCESS!
) else (
    echo .
    echo .   This setup program did not complete.
)
echo .
echo .
echo .
pause
