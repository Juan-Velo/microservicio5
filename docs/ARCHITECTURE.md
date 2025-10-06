# Arquitectura del Microservicio 5 - Orquestador

## Visión General

El Microservicio 5 actúa como un **orquestador** que consume y consolida información de múltiples microservicios backend, proporcionando endpoints unificados al frontend. Esto simplifica la arquitectura del cliente y mejora el rendimiento al reducir el número de llamadas HTTP.

## Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                           FRONTEND                               │
│                      (React/Vue/Angular)                         │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ HTTP Requests
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   MICROSERVICIO 5 - ORQUESTADOR                  │
│                        (Python/FastAPI)                          │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                 OrchestratorService                       │  │
│  │  • Llamadas paralelas (asyncio.gather)                   │  │
│  │  • Consolidación de datos                                │  │
│  │  • Cálculo de métricas agregadas                         │  │
│  │  • Manejo resiliente de errores                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌─────┐│
│  │MS1 Client    │  │MS2 Client    │  │MS3 Client    │  │MS4  ││
│  │(Users)       │  │(Accounts)    │  │(Metrics)     │  │Client│
│  └──────────────┘  └──────────────┘  └──────────────┘  └─────┘│
└─────┬──────────────────┬──────────────────┬──────────────┬─────┘
      │                  │                  │              │
      │ HTTP             │ HTTP             │ HTTP         │ HTTP
      │                  │                  │              │
      ▼                  ▼                  ▼              ▼
┌──────────┐      ┌──────────┐      ┌──────────┐   ┌──────────┐
│  MS 1    │      │  MS 2    │      │  MS 3    │   │  MS 4    │
│ Users &  │      │ Accounts │      │ TikTok   │   │Dashboard │
│  Auth    │      │  & Q&A   │      │ Metrics  │   │  Global  │
│ (Java/   │      │(Node.js/ │      │(Python/  │   │ (Java/   │
│ Spring)  │      │TypeScript│      │ FastAPI) │   │ Spring)  │
└──────────┘      └──────────┘      └──────────┘   └──────────┘
     │                  │                  │              │
     └──────────────────┴──────────────────┴──────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   Bases de Datos │
                    │   PostgreSQL,    │
                    │   MongoDB, etc.  │
                    └──────────────────┘
```

## Componentes Principales

### 1. Main Application (`main.py`)
- **Responsabilidad**: Punto de entrada de la aplicación FastAPI
- **Funciones**:
  - Definir endpoints REST
  - Configurar middleware (CORS)
  - Manejar excepciones
  - Documentación automática (Swagger/ReDoc)

### 2. OrchestratorService (`src/orchestrator_service.py`)
- **Responsabilidad**: Lógica de orquestación y consolidación
- **Funciones**:
  - Coordinar llamadas paralelas a múltiples microservicios
  - Consolidar respuestas
  - Calcular métricas agregadas
  - Generar rankings y tendencias
  - Manejo resiliente de errores

### 3. HTTP Clients (`src/clients.py`)
- **Responsabilidad**: Comunicación con microservicios externos
- **Componentes**:
  - `BaseClient`: Funcionalidad común (reintentos, timeouts)
  - `Microservice1Client`: Usuario y autenticación
  - `Microservice2Client`: Cuentas scrapeadas
  - `Microservice3Client`: Métricas de TikTok
  - `Microservice4Client`: Dashboard global

### 4. Models (`src/models.py`)
- **Responsabilidad**: Definición de esquemas de datos
- **Funciones**:
  - Validación de entrada/salida con Pydantic
  - Serialización JSON
  - Documentación automática de API

### 5. Configuration (`src/config.py`)
- **Responsabilidad**: Configuración centralizada
- **Contenido**:
  - URLs de microservicios
  - Timeouts y reintentos
  - Variables de entorno

## Flujo de Datos

### Endpoint: `/api/dashboard/consolidated`

```
1. Cliente hace request → GET /api/dashboard/consolidated?user_id=1

2. FastAPI recibe la petición y llama a OrchestratorService.get_consolidated_data()

3. OrchestratorService crea tareas paralelas:
   ├─ Task 1: MS1Client.get_user_profile(user_id=1)
   ├─ Task 2: MS2Client.get_scraped_accounts_by_user(user_id=1)
   ├─ Task 3: MS3Client.query_user_metrics(user_id=1)
   └─ Task 4: MS4Client.get_dashboard_info()

4. asyncio.gather() ejecuta todas las tareas en paralelo

5. OrchestratorService consolida las respuestas:
   ├─ Combina datos de usuarios
   ├─ Agrega cuentas scrapeadas
   ├─ Integra métricas de TikTok
   ├─ Incluye información del dashboard
   └─ Genera metadata (totales, estado de servicios)

6. Respuesta JSON consolidada se devuelve al cliente
```

### Endpoint: `/api/dashboard/summary`

```
1. Cliente hace request → GET /api/dashboard/summary

2. FastAPI llama a OrchestratorService.get_summary_data()

3. OrchestratorService:
   ├─ Llama internamente a get_consolidated_data()
   ├─ Calcula estadísticas resumidas (totales, promedios)
   ├─ Genera rankings:
   │  ├─ Top usuarios por número de cuentas
   │  ├─ Top cuentas por engagement
   │  └─ Posts con mejor rendimiento
   └─ Calcula tendencias de crecimiento

4. Respuesta JSON con resumen y rankings se devuelve al cliente
```

## Patrones de Diseño Implementados

### 1. **Orquestación (Orchestration Pattern)**
- Coordina múltiples llamadas a servicios
- Mantiene la lógica de negocio centralizada
- Simplifica la interacción del cliente

### 2. **Cliente HTTP Reutilizable**
- Clases cliente específicas para cada microservicio
- Lógica común en `BaseClient`
- Encapsulación de detalles de comunicación

### 3. **Llamadas Paralelas (Parallel Calls)**
- Uso de `asyncio.gather()` para ejecutar tareas concurrentemente
- Reduce significativamente el tiempo de respuesta
- Mejor uso de recursos

### 4. **Resiliencia (Resilience Pattern)**
- Reintentos automáticos con delay
- Manejo graceful de fallos (un servicio fallido no afecta a los demás)
- Logging detallado de errores
- Timeouts configurables

### 5. **Agregación de Datos (Data Aggregation)**
- Consolidación de datos de múltiples fuentes
- Cálculo de métricas derivadas
- Generación de metadata enriquecida

## Características de Rendimiento

### Optimización de Tiempo de Respuesta

**Sin orquestador (cliente hace 4 llamadas secuenciales):**
```
Time = T1 + T2 + T3 + T4
     = 500ms + 400ms + 600ms + 300ms
     = 1800ms
```

**Con orquestador (llamadas paralelas):**
```
Time = max(T1, T2, T3, T4)
     = max(500ms, 400ms, 600ms, 300ms)
     = 600ms
```

**Mejora: ~67% reducción en tiempo de respuesta**

### Manejo de Errores

El orquestador implementa manejo resiliente:
- Si MS1 falla → Continúa con MS2, MS3, MS4
- Si MS3 está lento → No bloquea a MS1, MS2, MS4
- Metadata indica qué servicios respondieron exitosamente

## Escalabilidad

### Horizontal Scaling
- Múltiples instancias del orquestador pueden ejecutarse en paralelo
- Load balancer distribuye peticiones
- Sin estado compartido (stateless)

### Vertical Scaling
- Aprovecha múltiples cores CPU con asyncio
- Pool de conexiones HTTP reutilizables
- Límites configurables de concurrencia

## Seguridad

### Implementaciones Actuales
- CORS configurado para permitir cross-origin requests
- Validación de entrada con Pydantic
- Manejo de excepciones centralizado

### Mejoras Futuras Recomendadas
- [ ] Autenticación JWT end-to-end
- [ ] Rate limiting por IP/usuario
- [ ] Validación de tokens antes de propagar a microservicios
- [ ] Encriptación de datos sensibles
- [ ] API Keys para acceso al orquestador

## Monitoreo y Observabilidad

### Logging
- Registro detallado de cada operación
- Logs estructurados con niveles (INFO, WARNING, ERROR)
- Contexto de peticiones (user_id, timestamps)

### Métricas Disponibles (futuro)
- Tiempo de respuesta por endpoint
- Tasa de éxito/fallo por microservicio
- Número de peticiones por minuto
- Latencia de red a cada microservicio

### Health Checks
- Endpoint `/` para verificar que el orquestador está vivo
- Endpoint `/api/health/services` para verificar estado de dependencias

## Extensibilidad

### Agregar Nuevo Microservicio

1. **Crear nuevo cliente**:
```python
# src/clients.py
class Microservice5Client(BaseClient):
    async def get_some_data(self):
        url = ENDPOINTS["microservice5"]["some_endpoint"]
        return await self._make_request("GET", url)
```

2. **Actualizar configuración**:
```python
# src/config.py
MICROSERVICE5_URL = os.getenv("MICROSERVICE5_URL", "http://localhost:8006")
ENDPOINTS["microservice5"] = {
    "some_endpoint": f"{MICROSERVICE5_URL}/api/data"
}
```

3. **Integrar en orquestador**:
```python
# src/orchestrator_service.py
self.ms5_client = Microservice5Client()

async def get_consolidated_data(self, user_id):
    tasks = [
        # ... tareas existentes
        self._get_new_data()
    ]
```

## Testing

### Pruebas Disponibles
- `tests/test_endpoints.py`: Tests manuales de endpoints
- Health checks de servicios
- Validación de respuestas

### Estrategia de Testing Recomendada
- Unit tests: Probar cada cliente individualmente
- Integration tests: Probar orquestación completa
- Mock services: Simular respuestas de microservicios
- Load testing: Validar rendimiento bajo carga

## Deployment

### Docker
```bash
docker build -t microservicio5 .
docker run -p 8005:8005 microservicio5
```

### Docker Compose
```bash
docker-compose up -d
```

### Variables de Entorno en Producción
```env
MICROSERVICE1_URL=http://ms1.production.com
MICROSERVICE2_URL=http://ms2.production.com
MICROSERVICE3_URL=http://ms3.production.com
MICROSERVICE4_URL=http://ms4.production.com
REQUEST_TIMEOUT=30
MAX_RETRIES=3
```

## Mejoras Futuras

1. **Cache distribuido** (Redis)
   - Cachear respuestas frecuentes
   - Reducir carga en microservicios backend
   - TTL configurable por endpoint

2. **Circuit Breaker**
   - Detectar servicios caídos
   - Evitar llamadas innecesarias
   - Fallback automático

3. **GraphQL**
   - Permitir al cliente especificar campos exactos
   - Reducir over-fetching
   - Queries más flexibles

4. **Streaming**
   - Server-Sent Events para actualizaciones en tiempo real
   - WebSockets para comunicación bidireccional

5. **Paginación**
   - Implementar paginación para grandes volúmenes
   - Cursor-based pagination
   - Límites configurables

## Conclusión

El Microservicio 5 proporciona una capa de orquestación eficiente que:
- ✅ Simplifica la arquitectura del frontend
- ✅ Optimiza el rendimiento con llamadas paralelas
- ✅ Maneja errores de forma resiliente
- ✅ Consolida información de múltiples fuentes
- ✅ Es fácilmente extensible
- ✅ Está listo para producción con Docker
