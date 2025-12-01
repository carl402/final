@echo off
echo 🎯 Asistente de Decisiones Empresariales - Monte Carlo
echo =====================================================
echo.

echo 📦 Verificando instalación de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado o no está en el PATH
    echo 💡 Instale Python desde https://python.org
    pause
    exit /b 1
)

echo ✅ Python encontrado
echo.

echo 📋 Instalando dependencias...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Error al instalar dependencias
    pause
    exit /b 1
)

echo ✅ Dependencias instaladas correctamente
echo.

echo 🚀 Iniciando sistema...
python main.py

pause