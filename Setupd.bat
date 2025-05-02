@echo off
setlocal

set "LIBRE_DIR=%APPDATA%\LibreOffice\4\user"
set "LIBRE_CODE"=docsfoxLO.py"
set "NP_DIR=%APPDATA%\Notepad++\plugins\config\PythonScript\scripts"
set "NP_CODE=docsfoxNP.py"
set "TRUE="
:: Check for existing installation of Docsfox LibreOffice plugin.
:: Offer to upgrade the plugin.
echo .
echo .
echo .
if not exist %LIBRE_DIR%\Scripts\python\docsfoxLO.py goto PROMPTLO
:: LO plugin already installed
echo . The Docsfox plugin for LibreOffice
echo . is already installed. 
echo .
echo . If you have downloaded a new version,
echo . you may update the Docsfox plugin now.
echo .
:: LO is installed, prompt to update.
set /p UPDATELO=. Do you want to update Docsfox? Enter Y or N: 
if /I %UPDATELO% NEQ Y goto PROMPTNP
:: User wants to update LO plugin
cls
echo .
echo . 
echo .
echo . To update the Docsfox plugin for LibreOffice,
echo .
echo . 1. In your Downloads folder, delete the files:
echo .    Setupd.bat
echo .    docsfoxLO.py
echo . 2. Open the new main-docsfox.zip and copy
echo .    Setupd.bat and docsfoxLO.py
echo .    to the Downloads folder.
echo . 3. Run Setupd.bat from the Downloads folder.
echo .
set /p READYUPDATELO=. Have you completed steps 1 and 2? Enter Y or N: 
if /I %READYUPDATELO% NEQ Y goto UPDATELONOTREADY
:: User is ready to update LO
goto SETUPLO
:: User wants to update plugin but is not ready.
:UPDATELONOTREADY
echo .
echo . Please complete steps 1 and 2.
echo . Then run Setupd.bat again to update
echo . the Docsfox plugin for LibreOffice.
echo .
pause
goto END

:PROMPTLO
:: docsfoxLO not installed
if exist %LIBRE_DIR% goto SETUPLO
echo .
echo .
echo . LibreOffice is not installed.
echo . Docsfox uses LibreOffice or Notepad++
echo . to assembly customized documents.
echo .
echo . Please install LibreOffice or Notepad++.
echo . Then run Setupd.bat again.
pause .
goto END
:: LibreOffice is currently installed.
echo .
echo .
echo .
if exist %~np0\docsfoxLO.py goto SETUPLO
echo .
echo .
echo .
echo . The plugin file, docsfoxLO.py, is not found.
echo . Please open main-docsfox.zip and copy
echo . docsfoxLO.py into the Downloads folder.
echo .
echo . Then run Setupd.bat again.
pause
goto END
:SETUPLO
cls
echo .
echo .
echo .
set /p ADDLO=. Add the Docsfox plugin to LibreOffice? Enter Y or N: 
if /I %ADDLO% NEQ y goto PROMPTNP
if not exist %~dp0\docsfoxLO.py (echo . 
echo .
echo . The plugin, docsfoxLO.py, was not found
echo . in the folder: %~dp0
echo . 
pause
goto MISSINGPLUGIN )
echo .
echo .
echo . Adding the Docsfox plugin to LibreOffice
echo .
echo .
echo .
C:
if not exist %LIBRE_DIR%\Scripts\ md %LIBRE_DIR%\Scripts
if not exist %LIBRE_DIR%\Scripts\python\ md %LIBRE_DIR%\scripts\python
copy %~dp0\docsfoxLO.py %LIBRE_DIR%\Scripts\python\
if exist %LIBRE_DIR%\Scripts\python\docsfoxLO.py echo . Success! The plugin was added to LibreOffice.
echo .
if not exist %LIBRE_DIR%\Scripts\python\docsfoxLO.py echo . Docsfox failed to add the LibreOffice plugin.
echo .
echo .
pause
goto END

:PROMPTNP
:: Check for existing installation of Docsfox Notepad++ plugin.
:: Offer to upgrade the plugin.
cls
echo .
echo .
echo .
if not exist %NP_DIR%\docsfoxNP.py goto SETUPNP
:: NP plugin already installed
echo . The Docsfox plugin for Notepad++
echo . is already installed. 
echo .
echo . If you have downloaded a new version,
echo . you may update the Docsfox plugin now.
echo .
:: NP is installed, prompt to update.
set /p UPDATENP=. Do you want to update the plugin? Enter Y or N: 
if /I %UPDATENP% NEQ Y goto NEITHER
:: User wants to update NP plugin
echo .
echo . 
echo .
echo . To update the Docsfox plugin for Notepad++,
echo . 1. In your Downloads folder, delete the files:
echo .    Setupd.bat
echo .    docsfoxNP.py
echo . 2. Open the new main-docsfox.zip and copy
echo .    Setupd.bat and docsfoxNP.py
echo .    to the Downloads folder.
echo . 3. Run Setupd.bat from the Downloads folder.
echo .
set /p READYUPDATENP=. Have you completed steps 1 and 2? Enter Y or N: 
if /I %READYUPDATENP% NEQ Y goto UPDATENPNOTREADY
:: User is ready to update NP
goto SETUPNP
:: User wants to update plugin but is not ready.
:UPDATENPNOTREADY
echo .
echo . Please complete steps 1 and 2.
echo . Then run Setupd.bat again to update
echo . the Docsfox plugin for Notepad++.
echo .
pause
goto END

:SETUPNP
cls
echo .
echo .
echo .
set /p ADDNP=. Add the Docsfox plugin to Notepad++? Enter Y or N: 
if /I %ADDNP% NEQ y goto NONP
if not exist %~dp0\docsfoxNP.py (echo . 
echo .
echo . The plugin, docsfoxNP.py, was not found
echo . in the folder: %~dp0
echo . 
pause
goto MISSINGPLUGIN )
echo .
echo .
echo . Adding the Docsfox plugin to Notepad++
echo .
echo .
pause
copy %~dp0\docsfoxNP.py "%NP_DIR%"
echo .
if exist %NP_DIR%\docsfoxNP.py echo . Success! The plugin was added to Notepad++.
echo .
if not exist %NP_DIR%\docsfoxNP.py echo . Docsfox failed to add the Notepad++ plugin.
echo .
echo .
pause
goto END

:MISSINGPLUGIN
cls
echo .
echo .
echo .
echo . To install Docsfox,
echo . you need to copy the plugin files,
echo . docsfoxLO.py and docsfoxNP.py,
echo . to the same folder where you have
echo . this setup file, Setupd.bat
echo .
echo . To copy the plugin files, double-click
echo . the download, main-docsfox.zip,
echo . find docsfoxLO.py and docsfoxNP.py,
echo . and copy them to the Downloads folder.
echo .
echo . Then run Setupd.bat again.
echo .
pause
goto END

:NEITHER
cls
echo .
echo .
echo .
echo . You chose not to add Docsfox to 
echo . either LibreOffice or Notepad++.
echo . If you already added the Docsfox
echo . plugin, you can continue using it.
echo .
echo . If you have not yet installed
echo . LibreOffice or Notepad++, you can
echo . get the downloads from our website.
echo .
echo . When you are ready to install Docsfox,
echo . be sure to copy docsfoxLO.py and docsfoxNP.py
echo . from the Docsfox download, main-docsfox.zip,
echo . to the same place as Setupd.bat.
echo .
echo . Questions? Contact us at Docsfox.com
pause
goto END
:END
