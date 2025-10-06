#!/bin/bash

# Script de inicio rápido para Microservicio 5 - Orquestador (Linux/Mac)
# Este script facilita la instalación y ejecución del microservicio

echo "======================================="
echo "Microservicio 5 - Orquestador"
echo "Script de Inicio Rápido"
echo "======================================="
echo ""

# Verificar que Python está instalado
echo "Verificando instalación de Python..."
if ! command -v python3 &> /dev/null; then
    echo "✗ Error: Python3 no está instalado"
    echo "Por favor, instala Python 3.9 o superior"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✓ Python encontrado: $PYTHON_VERSION"
echo ""

# Preguntar si quiere crear entorno virtual
read -p "¿Deseas crear un entorno virtual? (Recomendado) [S/n]: " CREATE_VENV
CREATE_VENV=${CREATE_VENV:-S}

if [[ $CREATE_VENV =~ ^[SsYy]$ ]]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
    
    echo "Activando entorno virtual..."
    source venv/bin/activate
    echo "✓ Entorno virtual activado"
fi

echo ""

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencias instaladas correctamente"
else
    echo "✗ Error al instalar dependencias"
    exit 1
fi

echo ""

# Verificar si existe archivo .env
if [ ! -f ".env" ]; then
    echo "⚠ Archivo .env no encontrado"
    echo "Se utilizarán los valores por defecto de configuración"
    echo "Para configurar URLs personalizadas, copia .env.example a .env"
fi

echo ""

# Preguntar si quiere iniciar el servicio
read -p "¿Deseas iniciar el servicio ahora? [S/n]: " START_SERVICE
START_SERVICE=${START_SERVICE:-S}

if [[ $START_SERVICE =~ ^[SsYy]$ ]]; then
    echo ""
    echo "======================================="
    echo "Iniciando Microservicio 5..."
    echo "======================================="
    echo ""
    echo "El servicio estará disponible en:"
    echo "  - URL: http://localhost:8005"
    echo "  - Documentación Swagger: http://localhost:8005/docs"
    echo "  - Documentación ReDoc: http://localhost:8005/redoc"
    echo ""
    echo "Presiona Ctrl+C para detener el servicio"
    echo ""
    
    python3 main.py
else
    echo ""
    echo "Para iniciar el servicio manualmente, ejecuta:"
    echo "  python3 main.py"
    echo ""
    echo "O usando uvicorn directamente:"
    echo "  uvicorn main:app --host 0.0.0.0 --port 8005 --reload"
    echo ""
fi
