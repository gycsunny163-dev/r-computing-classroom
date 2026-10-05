@echo off
setlocal
chcp 65001 >nul
set "REPO=%~dp0"
set "CONTROL=%LOCALAPPDATA%\RClassroom-v1"
set "RUNTIME=%LOCALAPPDATA%\RClassroom-v1"
if defined R_CLASSROOM_RUNTIME set "RUNTIME=%R_CLASSROOM_RUNTIME%"
if not defined R_CLASSROOM_RUNTIME if exist "%CONTROL%\runtime-path.txt" set /p "RUNTIME="<"%CONTROL%\runtime-path.txt"
if not exist "%RUNTIME%\Library\bin" mkdir "%RUNTIME%\Library\bin"
if errorlevel 1 goto fail
if exist "%RUNTIME%\Library\bin\micromamba.exe" goto environment
curl.exe --fail --location --silent --show-error https://micro.mamba.pm/api/micromamba/win-64/latest -o "%RUNTIME%\micromamba.tar.bz2"
if errorlevel 1 goto fail
tar.exe -xjf "%RUNTIME%\micromamba.tar.bz2" -C "%RUNTIME%" Library/bin/micromamba.exe
if errorlevel 1 goto fail
:environment
if exist "%RUNTIME%\environment\python.exe" goto configure
"%RUNTIME%\Library\bin\micromamba.exe" create --yes --no-rc --root-prefix "%RUNTIME%\mamba-root" --prefix "%RUNTIME%\environment" --file "%REPO%environment.yml"
if errorlevel 1 goto fail
:configure
"%RUNTIME%\Library\bin\micromamba.exe" --no-rc --root-prefix "%RUNTIME%\mamba-root" run --prefix "%RUNTIME%\environment" python "%REPO%tools\setup_local.py" --runtime "%RUNTIME%"
if errorlevel 1 goto fail
if not exist "%CONTROL%" mkdir "%CONTROL%"
<nul set /p "=%RUNTIME%">"%CONTROL%\runtime-path.txt"
echo Ready. Open start-windows.cmd to enter the classroom.
if not defined CI pause
exit /b 0
:fail
echo Setup failed. Keep this error text for diagnosis.
if not defined CI pause
exit /b 1
