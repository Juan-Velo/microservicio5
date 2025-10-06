# Microservicio 5 - Orquestador

## Descripción

Microservicio orquestador en Python que actúa como intermediario entre el frontend y múltiples microservicios backend. Consolida información de diferentes fuentes y la entrega lista para su consumo, evitando que el frontend tenga que realizar múltiples llamadas.

## Arquitectura

Este microservicio **NO tiene base de datos propia**. Su función es orquestar llamadas a otros microservicios:

- **Microservicio 1** (Java/Spring Boot): Gestión de usuarios y autenticación
- **Microservicio 2** (Node.js/TypeScript): Cuentas scrapeadas y preguntas
- **Microservicio 3** (Python/FastAPI): Métricas de TikTok y queries
- **Microservicio 4** (Java/Spring Boot): Dashboard global

## Estructura del Proyecto

```
microservicio5/
├── main.py                          # Punto de entrada de la aplicación
├── requirements.txt                 # Dependencias de Python
├── Dockerfile                       # Configuración de Docker
├── README.md                        # Este archivo
└── src/
    ├── __init__.py
    ├── config.py                    # Configuración de URLs y constantes
    ├── models.py                    # Modelos de datos Pydantic
    ├── clients.py                   # Clientes HTTP para cada microservicio
    └── orchestrator_service.py      # Lógica de orquestación
```

## Endpoints Disponibles

### 1. Health Check
```
GET /
```

Verifica que el servicio está activo.

**Respuesta:**
```json
{
  "status": "ok",
  "service": "Microservicio 5 - Orquestador",
  "version": "1.0.0",
  "message": "Service is running"
}
```

---

### 2. Dashboard Consolidado
```
GET /api/dashboard/consolidated?user_id={user_id}
```

Obtiene información consolidada de todos los microservicios.

**Parámetros:**
- `user_id` (opcional): ID del usuario para filtrar información específica

**Respuesta:**
```json
{
  "users": [
    {
      "id": 1,
      "email": "user@example.com",
      "role": "USER",
      "created_at": "2025-01-15T10:30:00"
    }
  ],
  "scraped_accounts": [
    {
      "id": 1,
      "account_name": "@tiktoker123",
      "user_id": 1,
      "created_at": "2025-01-20T15:45:00"
    }
  ],
  "metrics": {
    "items": [
      {
        "postId": "7123456789",
        "usernameTiktokAccount": "@tiktoker123",
        "views": 150000,
        "likes": 12000,
        "engagement": 8.5,
        "datePosted": "2025-01-22"
      }
    ],
    "count": 150,
    "dashboard": [
      {
        "metric": "totals",
        "totalPosts": 150,
        "totalViews": 5000000,
        "totalLikes": 450000,
        "avgEngagement": 8.2
      }
    ]
  },
  "dashboard_data": [
    {
      "username": "@tiktoker123",
      "totalViews": 5000000
    }
  ],
  "metadata": {
    "total_users": 10,
    "total_accounts": 25,
    "total_posts_analyzed": 150,
    "timestamp": "2025-10-05T12:00:00",
    "services_status": {
      "microservice1": "ok",
      "microservice2": "ok",
      "microservice3": "ok",
      "microservice4": "ok"
    }
  }
}
```

**Descripción:**
- Consume datos de **Microservicio 1** (usuarios)
- Consume datos de **Microservicio 2** (cuentas scrapeadas)
- Consume datos de **Microservicio 3** (métricas de TikTok)
- Consume datos de **Microservicio 4** (dashboard global)
- Todas las llamadas se realizan **en paralelo** para optimizar el tiempo de respuesta
- Incluye metadata con información agregada y estado de los servicios

---

### 3. Resumen y Rankings
```
GET /api/dashboard/summary?user_id={user_id}
```

Proporciona un resumen estadístico y rankings de las métricas.

**Parámetros:**
- `user_id` (opcional): ID del usuario para filtrar información específica

**Respuesta:**
```json
{
  "summary": {
    "total_users": 10,
    "total_accounts": 25,
    "average_engagement": 8.5,
    "total_views": 5000000,
    "total_likes": 450000,
    "total_interactions": 550000
  },
  "rankings": {
    "top_users": [
      {
        "user_id": 1,
        "accounts_count": 5,
        "email": "user@example.com"
      }
    ],
    "top_accounts": [
      {
        "account": "@tiktoker123",
        "total_views": 1500000,
        "total_likes": 120000,
        "total_engagement": 45.2,
        "post_count": 50
      }
    ],
    "best_engagement": [
      {
        "post_id": "7123456789",
        "account": "@tiktoker123",
        "engagement": 15.8,
        "views": 250000,
        "likes": 35000
      }
    ]
  },
  "trends": {
    "growth_rate": 15.2,
    "engagement_trend": "increasing"
  },
  "timestamp": "2025-10-05T12:00:00"
}
```

**Descripción:**
- Calcula estadísticas resumidas de todos los datos consolidados
- Genera rankings de:
  - Top 5 usuarios más activos (por número de cuentas)
  - Top 5 cuentas con mejor engagement
  - Top 5 posts con mejor engagement
- Analiza tendencias de crecimiento
- Utiliza los datos consolidados del endpoint principal

---

### 4. Estado de Servicios
```
GET /api/health/services
```

Verifica el estado de conexión con todos los microservicios.

**Respuesta:**
```json
{
  "microservice1": "healthy",
  "microservice2": "healthy",
  "microservice3": "healthy",
  "microservice4": "healthy"
}
```

---

## Instalación y Ejecución

### Requisitos Previos

- Python 3.9 o superior
- pip (gestor de paquetes de Python)

### Instalación Local

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configurar variables de entorno (opcional):**
   
   Crear archivo `.env` en la raíz del proyecto:
   ```env
   MICROSERVICE1_URL=http://localhost:8081
   MICROSERVICE2_URL=http://localhost:3000
   MICROSERVICE3_URL=http://localhost:8000
   MICROSERVICE4_URL=http://localhost:8080
   REQUEST_TIMEOUT=30
   MAX_RETRIES=3
   ```

3. **Ejecutar el servicio:**
   ```bash
   python main.py
   ```

   O usando uvicorn directamente:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8005 --reload
   ```

4. **Acceder a la documentación interactiva:**
   - Swagger UI: http://localhost:8005/docs
   - ReDoc: http://localhost:8005/redoc

### Ejecución con Docker

1. **Construir la imagen:**
   ```bash
   docker build -t microservicio5 .
   ```

2. **Ejecutar el contenedor:**
   ```bash
   docker run -p 8005:8005 microservicio5
   ```

---

## Configuración

Las URLs de los microservicios se configuran mediante variables de entorno en `src/config.py`:

| Variable | Valor por Defecto | Descripción |
|----------|-------------------|-------------|
| `MICROSERVICE1_URL` | `http://localhost:8081` | URL del microservicio de usuarios |
| `MICROSERVICE2_URL` | `http://localhost:3000` | URL del microservicio de cuentas |
| `MICROSERVICE3_URL` | `http://localhost:8000` | URL del microservicio de métricas |
| `MICROSERVICE4_URL` | `http://localhost:8080` | URL del microservicio de dashboard |
| `REQUEST_TIMEOUT` | `30` | Timeout en segundos para peticiones HTTP |
| `MAX_RETRIES` | `3` | Número máximo de reintentos en caso de fallo |

---

## Lógica de Orquestación

### Llamadas Paralelas

El servicio realiza llamadas **asíncronas y paralelas** a los microservicios usando `asyncio.gather()`, lo que optimiza el tiempo de respuesta:

```python
tasks = [
    self._get_users_data(user_id),
    self._get_scraped_accounts_data(user_id),
    self._get_metrics_data(user_id),
    self._get_dashboard_data()
]
results = await asyncio.gather(*tasks, return_exceptions=True)
```

### Manejo de Errores Resiliente

Si un microservicio falla:
- Se registra el error en los logs
- Los demás microservicios continúan ejecutándose
- Se devuelven datos parciales al frontend
- El estado del servicio fallido se refleja en la metadata

### Reintentos Automáticos

Cada cliente HTTP implementa reintentos automáticos con delay exponencial para manejar fallos temporales de red.

---

## Tecnologías Utilizadas

- **FastAPI**: Framework web moderno y de alto rendimiento
- **Uvicorn**: Servidor ASGI para FastAPI
- **httpx**: Cliente HTTP asíncrono para Python
- **Pydantic**: Validación de datos y serialización
- **asyncio**: Programación asíncrona para llamadas paralelas

---

## Ejemplos de Uso

### Obtener Dashboard Consolidado (sin filtro)
```bash
curl http://localhost:8005/api/dashboard/consolidated
```

### Obtener Dashboard Consolidado (filtrado por usuario)
```bash
curl http://localhost:8005/api/dashboard/consolidated?user_id=1
```

### Obtener Resumen y Rankings
```bash
curl http://localhost:8005/api/dashboard/summary
```

### Verificar Estado del Servicio
```bash
curl http://localhost:8005/
```

### Verificar Estado de Microservicios
```bash
curl http://localhost:8005/api/health/services
```

---

## Notas Importantes

1. **Autenticación**: Algunos endpoints de los microservicios requieren tokens de autenticación. Actualmente, el orquestador no maneja autenticación, pero puede extenderse para incluir este soporte.

2. **Caching**: Para mejorar el rendimiento en producción, se puede implementar un sistema de cache (Redis, por ejemplo) para almacenar respuestas temporalmente.

3. **Rate Limiting**: Considerar implementar rate limiting para proteger el servicio de sobrecarga.

4. **Monitoreo**: Se recomienda implementar herramientas de monitoreo (Prometheus, Grafana) para observar el rendimiento y detectar problemas.

---

## Desarrollo Futuro

- [ ] Implementar autenticación y propagación de tokens
- [ ] Agregar cache distribuido con Redis
- [ ] Implementar circuit breaker pattern para fallos de servicios
- [ ] Agregar métricas de observabilidad (Prometheus)
- [ ] Implementar rate limiting
- [ ] Agregar más filtros y opciones de consulta
- [ ] Implementar paginación para grandes volúmenes de datos

---

## Autor

Microservicio desarrollado para el proyecto de Cloud Computing - UTEC 2025-2

## Licencia

Este proyecto es parte de un trabajo académico.
