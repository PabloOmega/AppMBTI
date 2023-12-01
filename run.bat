@echo off

setlocal enabledelayedexpansion

:: Entorno virtual
set VIRTUAL_ENV_NAME=env_django

:: Directorio actual del archivo .bat
set SCRIPT_DIR=%~dp0

:: Ruta completa del entorno virtual
set VIRTUAL_ENV_PATH=%SCRIPT_DIR%\%VIRTUAL_ENV_NAME%

:: Ruta de manage.py
set app_path=%SCRIPT_DIR%\manage.py

:: Activar el entorno virtual
call "%VIRTUAL_ENV_PATH%\Scripts\activate"

call "open_page.bat"
:: Ejecutar el servidor
python "%app_path%" runserver