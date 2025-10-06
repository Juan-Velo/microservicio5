"""
Script de verificación de la instalación del Microservicio 5.
Verifica que todas las dependencias estén instaladas correctamente.
"""

import sys
import importlib

# Lista de dependencias requeridas
REQUIRED_PACKAGES = [
    ("fastapi", "FastAPI"),
    ("uvicorn", "Uvicorn"),
    ("httpx", "httpx"),
    ("pydantic", "Pydantic"),
]

def check_python_version():
    """Verifica la versión de Python"""
    version = sys.version_info
    print(f"\n{'='*60}")
    print("VERIFICACIÓN DE PYTHON")
    print(f"{'='*60}")
    print(f"Versión de Python: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ ERROR: Se requiere Python 3.9 o superior")
        return False
    else:
        print("✅ Versión de Python correcta")
        return True

def check_packages():
    """Verifica que todos los paquetes estén instalados"""
    print(f"\n{'='*60}")
    print("VERIFICACIÓN DE DEPENDENCIAS")
    print(f"{'='*60}")
    
    all_installed = True
    
    for package_name, display_name in REQUIRED_PACKAGES:
        try:
            importlib.import_module(package_name)
            print(f"✅ {display_name} instalado correctamente")
        except ImportError:
            print(f"❌ {display_name} NO está instalado")
            all_installed = False
    
    return all_installed

def check_files():
    """Verifica que los archivos principales existan"""
    import os
    
    print(f"\n{'='*60}")
    print("VERIFICACIÓN DE ARCHIVOS")
    print(f"{'='*60}")
    
    required_files = [
        "main.py",
        "requirements.txt",
        "src/clients.py",
        "src/config.py",
        "src/models.py",
        "src/orchestrator_service.py",
        "Dockerfile",
        "README.md"
    ]
    
    all_exist = True
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} NO encontrado")
            all_exist = False
    
    return all_exist

def main():
    """Ejecuta todas las verificaciones"""
    print("\n" + "="*60)
    print("VERIFICACIÓN DE INSTALACIÓN - MICROSERVICIO 5")
    print("="*60)
    
    python_ok = check_python_version()
    packages_ok = check_packages()
    files_ok = check_files()
    
    print(f"\n{'='*60}")
    print("RESUMEN")
    print(f"{'='*60}")
    
    if python_ok and packages_ok and files_ok:
        print("\n✅ ¡Todo está correcto! El microservicio está listo para ejecutarse.")
        print("\nPara iniciar el servicio, ejecuta:")
        print("  python main.py")
        print("\nO usando el script de inicio:")
        print("  Windows: .\\start.ps1")
        print("  Linux/Mac: ./start.sh")
        return 0
    else:
        print("\n❌ Hay problemas con la instalación.")
        if not python_ok:
            print("\n• Actualiza Python a la versión 3.9 o superior")
        if not packages_ok:
            print("\n• Instala las dependencias con: pip install -r requirements.txt")
        if not files_ok:
            print("\n• Verifica que todos los archivos del proyecto estén presentes")
        return 1

if __name__ == "__main__":
    sys.exit(main())
