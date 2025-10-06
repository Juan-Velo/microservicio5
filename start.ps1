# Script de inicio rápido para Microservicio 5 - Orquestador
# Este script facilita la instalación y ejecución del microservicio

Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "Microservicio 5 - Orquestador" -ForegroundColor Cyan
Write-Host "Script de Inicio Rápido" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""

# Verificar que Python está instalado
Write-Host "Verificando instalación de Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Error: Python no está instalado o no está en el PATH" -ForegroundColor Red
    Write-Host "Por favor, instala Python 3.9 o superior desde https://www.python.org/" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Preguntar si quiere crear entorno virtual
Write-Host "¿Deseas crear un entorno virtual? (Recomendado) [S/n]: " -ForegroundColor Yellow -NoNewline
$createVenv = Read-Host
if ($createVenv -eq "" -or $createVenv -eq "S" -or $createVenv -eq "s" -or $createVenv -eq "Y" -or $createVenv -eq "y") {
    Write-Host "Creando entorno virtual..." -ForegroundColor Yellow
    python -m venv venv
    
    Write-Host "Activando entorno virtual..." -ForegroundColor Yellow
    & .\venv\Scripts\Activate.ps1
    Write-Host "✓ Entorno virtual activado" -ForegroundColor Green
}

Write-Host ""

# Instalar dependencias
Write-Host "Instalando dependencias..." -ForegroundColor Yellow
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Dependencias instaladas correctamente" -ForegroundColor Green
} else {
    Write-Host "✗ Error al instalar dependencias" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Verificar si existe archivo .env
if (-Not (Test-Path ".env")) {
    Write-Host "⚠ Archivo .env no encontrado" -ForegroundColor Yellow
    Write-Host "Se utilizarán los valores por defecto de configuración" -ForegroundColor Yellow
    Write-Host "Para configurar URLs personalizadas, copia .env.example a .env" -ForegroundColor Yellow
}

Write-Host ""

# Preguntar si quiere iniciar el servicio
Write-Host "¿Deseas iniciar el servicio ahora? [S/n]: " -ForegroundColor Yellow -NoNewline
$startService = Read-Host
if ($startService -eq "" -or $startService -eq "S" -or $startService -eq "s" -or $startService -eq "Y" -or $startService -eq "y") {
    Write-Host ""
    Write-Host "=======================================" -ForegroundColor Cyan
    Write-Host "Iniciando Microservicio 5..." -ForegroundColor Cyan
    Write-Host "=======================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "El servicio estará disponible en:" -ForegroundColor Green
    Write-Host "  - URL: http://localhost:8005" -ForegroundColor Green
    Write-Host "  - Documentación Swagger: http://localhost:8005/docs" -ForegroundColor Green
    Write-Host "  - Documentación ReDoc: http://localhost:8005/redoc" -ForegroundColor Green
    Write-Host ""
    Write-Host "Presiona Ctrl+C para detener el servicio" -ForegroundColor Yellow
    Write-Host ""
    
    python main.py
} else {
    Write-Host ""
    Write-Host "Para iniciar el servicio manualmente, ejecuta:" -ForegroundColor Cyan
    Write-Host "  python main.py" -ForegroundColor White
    Write-Host ""
    Write-Host "O usando uvicorn directamente:" -ForegroundColor Cyan
    Write-Host "  uvicorn main:app --host 0.0.0.0 --port 8005 --reload" -ForegroundColor White
    Write-Host ""
}
