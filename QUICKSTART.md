# Microservicio 5 - Guía de Inicio Rápido

## 🚀 Instalación y Ejecución en 3 Pasos

### Opción 1: Script Automático (Recomendado)

#### Windows (PowerShell):
```powershell
.\start.ps1
```

#### Linux/Mac:
```bash
chmod +x start.sh
./start.sh
```

### Opción 2: Manual

#### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

#### 2. Ejecutar el servicio
```bash
python main.py
```

#### 3. Acceder a la documentación
- **Swagger UI**: http://localhost:8005/docs
- **ReDoc**: http://localhost:8005/redoc

---

## 📋 Endpoints Disponibles

### ✅ Health Check
```bash
GET http://localhost:8005/
```
Verifica que el servicio está activo.

### 📊 Dashboard Consolidado
```bash
GET http://localhost:8005/api/dashboard/consolidated
GET http://localhost:8005/api/dashboard/consolidated?user_id=1
```
Obtiene información consolidada de todos los microservicios.

### 📈 Resumen y Rankings
```bash
GET http://localhost:8005/api/dashboard/summary
GET http://localhost:8005/api/dashboard/summary?user_id=1
```
Proporciona resumen estadístico y rankings.

### 🏥 Estado de Servicios
```bash
GET http://localhost:8005/api/health/services
```
Verifica el estado de conexión con todos los microservicios.

---

## 🔧 Configuración

### Variables de Entorno

Crea un archivo `.env` (opcional):

```env
MICROSERVICE1_URL=http://localhost:8081
MICROSERVICE2_URL=http://localhost:3000
MICROSERVICE3_URL=http://localhost:8000
MICROSERVICE4_URL=http://localhost:8080
REQUEST_TIMEOUT=30
MAX_RETRIES=3
```

---

## 🐳 Docker

### Construir y ejecutar:
```bash
docker build -t microservicio5 .
docker run -p 8005:8005 microservicio5
```

### Docker Compose:
```bash
docker-compose up -d
```

---

## 🧪 Pruebas

Ejecutar pruebas de endpoints:

```bash
python tests/test_endpoints.py
```

---

## 📖 Documentación Completa

- **README.md**: Documentación completa del microservicio
- **docs/ARCHITECTURE.md**: Arquitectura y patrones de diseño
- **docs/response_examples.json**: Ejemplos de respuestas JSON

---

## 🎯 Características Principales

✅ **Orquestación**: Consume datos de 4 microservicios diferentes
✅ **Llamadas Paralelas**: Optimización de tiempo de respuesta (~67% más rápido)
✅ **Resiliencia**: Manejo graceful de fallos
✅ **Sin Base de Datos**: Actúa solo como orquestador
✅ **API REST**: Endpoints claros y documentados
✅ **Docker Ready**: Listo para contenedorización
✅ **Modular**: Código limpio y fácil de extender

---

## 📞 Microservicios Consumidos

| Microservicio | Función | Puerto |
|---------------|---------|--------|
| MS1 | Usuarios y Autenticación | 8081 |
| MS2 | Cuentas Scrapeadas | 3000 |
| MS3 | Métricas de TikTok | 8000 |
| MS4 | Dashboard Global | 8080 |

---

## ⚡ Ejemplo de Uso con cURL

```bash
# Health Check
curl http://localhost:8005/

# Dashboard Consolidado
curl http://localhost:8005/api/dashboard/consolidated

# Dashboard con filtro de usuario
curl http://localhost:8005/api/dashboard/consolidated?user_id=1

# Resumen y Rankings
curl http://localhost:8005/api/dashboard/summary

# Estado de Servicios
curl http://localhost:8005/api/health/services
```

---

## 🛠️ Stack Tecnológico

- **Python 3.9+**
- **FastAPI**: Framework web moderno
- **Uvicorn**: Servidor ASGI
- **httpx**: Cliente HTTP asíncrono
- **Pydantic**: Validación de datos
- **asyncio**: Programación asíncrona

---

## 📚 Estructura del Proyecto

```
microservicio5/
├── main.py                      # Punto de entrada
├── requirements.txt             # Dependencias
├── Dockerfile                   # Configuración Docker
├── docker-compose.yml           # Orquestación Docker
├── README.md                    # Documentación principal
├── src/
│   ├── clients.py              # Clientes HTTP
│   ├── config.py               # Configuración
│   ├── models.py               # Modelos de datos
│   └── orchestrator_service.py # Lógica de orquestación
├── docs/
│   ├── ARCHITECTURE.md         # Arquitectura detallada
│   └── response_examples.json  # Ejemplos de respuestas
└── tests/
    └── test_endpoints.py       # Tests de endpoints
```

---

## 💡 Próximos Pasos

1. ✅ Verificar que los microservicios 1-4 están corriendo
2. ✅ Ejecutar el microservicio 5
3. ✅ Probar endpoints con Swagger UI
4. ✅ Integrar con el frontend

---

## 🐛 Troubleshooting

**Problema**: "ModuleNotFoundError: No module named 'fastapi'"
- **Solución**: `pip install -r requirements.txt`

**Problema**: "Connection refused" al consumir microservicios
- **Solución**: Verificar que los microservicios 1-4 están corriendo en los puertos configurados

**Problema**: Puerto 8005 ya en uso
- **Solución**: Cambiar el puerto en `main.py` o detener el proceso que usa el puerto

---

## 📝 Notas

- El servicio NO requiere base de datos
- Actúa como intermediario entre frontend y backend
- Todas las llamadas a microservicios son asíncronas y paralelas
- Manejo resiliente: si un servicio falla, los demás continúan

---

**Desarrollado para Cloud Computing - UTEC 2025-2**
