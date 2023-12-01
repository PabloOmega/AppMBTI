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

:: Comprobación de Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python no esta instalado. Por favor, instala Python.
    pause
    exit /b 1
) else (
    echo Python instalado. Por favor espere mientras se instala la aplicación
)

:: Crear el entorno virtual
python -m venv %VIRTUAL_ENV_NAME%

:: Activar el entorno virtual
call "%VIRTUAL_ENV_PATH%\Scripts\activate"

:: Instalar paquetes
pip install -r requirements.txt

python "%app_path%" makemigrations
python "%app_path%" migrate

call "open_page.bat"
:: Ejecutar el servidor
python "%app_path%" runserver

:: Desactivar el entorno virtual
deactivate
