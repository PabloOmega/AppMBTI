@echo off

setlocal enabledelayedexpansion

set "ruta_del_ejecutable=wkhtmltox-0.12.6-1.msvc2015-win64.exe"

:: Verifica si el archivo ejecutable existe
if not exist "%ruta_del_ejecutable%" (
    echo El archivo ejecutable no se encuentra en la ruta especificada.
    pause
    exit /b
)

echo Espere mientras se instala wkhtmltox, dar clic en siguiente hasta el final, ¡NO CAMBIE LA RUTA POR DEFECTO!
echo Una vez instalado el wkhtmltox, continue con el proceso de instalación presionando aquí cualquier tecla
pause

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
