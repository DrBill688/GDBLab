@echo off
for %%a in ("%CD%") do set "parent=%%~nxa"

set venvname=%parent%_venv
set installdeps=N
set forcedeps=N

set /p venvname=Python venv name? [%venvname%]

echo Checking if %venvname% exists...
if not exist %UserProfile%\%venvname%\ (
    echo "    Creating..."
    call python -m venv %UserProfile%\%venvname%
    set forcedeps=Y
    set installdeps=Y
) else echo "    Exists."

echo Activating %venvname%
call %UserProfile%\%venvname%\scripts\activate.bat

echo Checking for PIP upgrade
call python -m pip install --upgrade pip

if "%forcedeps%" == "N" set /p installdeps="Do you want to refresh dependencies? (Y/N) [%installdeps%]"
echo %installdeps% | findstr "^[Yy]*$" > NUL
if %errorlevel% == 1 goto startapp

echo "About to clear the venv and rebuild it.  If this is in error, now is the time to CTRL-C"
pause

pip freeze > venvpiplist.txt
pip uninstall -y -r venvpiplist.txt
del venvpiplist.txt

:startapp
pip install -r requirements.txt
python wsgi.py
