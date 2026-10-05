@echo off
setlocal
chcp 65001 >nul
set "REPO=%~dp0"
set "CONTROL=%LOCALAPPDATA%\RClassroom-v1"
set "RUNTIME=%LOCALAPPDATA%\RClassroom-v1"
if defined R_CLASSROOM_RUNTIME set "RUNTIME=%R_CLASSROOM_RUNTIME%"
if not defined R_CLASSROOM_RUNTIME if exist "%CONTROL%\runtime-path.txt" set /p "RUNTIME="<"%CONTROL%\runtime-path.txt"
if exist "%RUNTIME%\environment\python.exe" goto run
call "%REPO%setup-windows.cmd"
if errorlevel 1 goto fail
:run
"%RUNTIME%\Library\bin\micromamba.exe" --no-rc --root-prefix "%RUNTIME%\mamba-root" run --prefix "%RUNTIME%\environment" python "%REPO%tools\classroom.py" --runtime "%RUNTIME%"
if errorlevel 1 goto fail
exit /b 0
:fail
echo Classroom action failed. Keep this error text for diagnosis.
pause
exit /b 1
