# Guía de Prueba de Endpoints - Microservicio 5

## Colección de Requests para Testing Manual

Esta guía proporciona comandos curl listos para usar para probar cada endpoint del microservicio.

---

## 1. Health Check

### Verificar que el servicio está activo

**Request:**
```bash
curl -X GET http://localhost:8005/ -H "Content-Type: application/json"
```

**Respuesta Esperada (200 OK):**
```json
{
  "status": "ok",
  "service": "Microservicio 5 - Orquestador",
  "version": "1.0.0",
  "message": "Service is running"
}
```

---

## 2. Dashboard Consolidado (Sin Filtro)

### Obtener información consolidada de todos los usuarios

**Request:**
```bash
curl -X GET http://localhost:8005/api/dashboard/consolidated -H "Content-Type: application/json"
```

**Respuesta Esperada (200 OK):**
```json
{
  "users": [...],
  "scraped_accounts": [...],
  "metrics": {
    "items": [...],
    "count": 150,
    "dashboard": [...]
  },
  "dashboard_data": [...],
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

---

## 3. Dashboard Consolidado (Filtrado por Usuario)

### Obtener información de un usuario específico

**Request:**
```bash
curl -X GET "http://localhost:8005/api/dashboard/consolidated?user_id=1" -H "Content-Type: application/json"
```

**Parámetros:**
- `user_id`: ID del usuario (ejemplo: 1)

**Respuesta Esperada (200 OK):**
Similar al endpoint anterior, pero filtrado para el usuario especificado.

---

## 4. Resumen y Rankings (Sin Filtro)

### Obtener resumen estadístico y rankings globales

**Request:**
```bash
curl -X GET http://localhost:8005/api/dashboard/summary -H "Content-Type: application/json"
```

**Respuesta Esperada (200 OK):**
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

---

## 5. Resumen y Rankings (Filtrado por Usuario)

### Obtener resumen de un usuario específico

**Request:**
```bash
curl -X GET "http://localhost:8005/api/dashboard/summary?user_id=1" -H "Content-Type: application/json"
```

**Parámetros:**
- `user_id`: ID del usuario (ejemplo: 1)

---

## 6. Estado de Servicios

### Verificar la salud de todos los microservicios conectados

**Request:**
```bash
curl -X GET http://localhost:8005/api/health/services -H "Content-Type: application/json"
```

**Respuesta Esperada (200 OK) - Todos Saludables:**
```json
{
  "microservice1": "healthy",
  "microservice2": "healthy",
  "microservice3": "healthy",
  "microservice4": "healthy"
}
```

**Respuesta con Fallos:**
```json
{
  "microservice1": "healthy",
  "microservice2": "unhealthy: Connection timeout",
  "microservice3": "healthy",
  "microservice4": "unhealthy: Service unavailable"
}
```

---

## Testing con PowerShell (Windows)

### Script para probar todos los endpoints

```powershell
# Health Check
Write-Host "1. Probando Health Check..." -ForegroundColor Cyan
Invoke-WebRequest -Uri "http://localhost:8005/" -Method GET | Select-Object -ExpandProperty Content

Start-Sleep -Seconds 1

# Dashboard Consolidado
Write-Host "`n2. Probando Dashboard Consolidado..." -ForegroundColor Cyan
Invoke-WebRequest -Uri "http://localhost:8005/api/dashboard/consolidated" -Method GET | Select-Object -ExpandProperty Content

Start-Sleep -Seconds 1

# Dashboard con filtro
Write-Host "`n3. Probando Dashboard Consolidado (user_id=1)..." -ForegroundColor Cyan
Invoke-WebRequest -Uri "http://localhost:8005/api/dashboard/consolidated?user_id=1" -Method GET | Select-Object -ExpandProperty Content

Start-Sleep -Seconds 1

# Resumen
Write-Host "`n4. Probando Resumen y Rankings..." -ForegroundColor Cyan
Invoke-WebRequest -Uri "http://localhost:8005/api/dashboard/summary" -Method GET | Select-Object -ExpandProperty Content

Start-Sleep -Seconds 1

# Estado de servicios
Write-Host "`n5. Probando Estado de Servicios..." -ForegroundColor Cyan
Invoke-WebRequest -Uri "http://localhost:8005/api/health/services" -Method GET | Select-Object -ExpandProperty Content
```

---

## Testing con Bash (Linux/Mac)

### Script para probar todos los endpoints

```bash
#!/bin/bash

echo "1. Probando Health Check..."
curl -s http://localhost:8005/ | jq .

sleep 1

echo -e "\n2. Probando Dashboard Consolidado..."
curl -s http://localhost:8005/api/dashboard/consolidated | jq .

sleep 1

echo -e "\n3. Probando Dashboard Consolidado (user_id=1)..."
curl -s "http://localhost:8005/api/dashboard/consolidated?user_id=1" | jq .

sleep 1

echo -e "\n4. Probando Resumen y Rankings..."
curl -s http://localhost:8005/api/dashboard/summary | jq .

sleep 1

echo -e "\n5. Probando Estado de Servicios..."
curl -s http://localhost:8005/api/health/services | jq .
```

---

## Testing con Python (Script Automatizado)

Ya está disponible en `tests/test_endpoints.py`:

```bash
python tests/test_endpoints.py
```

---

## Códigos de Estado HTTP

| Código | Descripción | Cuándo ocurre |
|--------|-------------|---------------|
| 200 | OK | Petición exitosa |
| 400 | Bad Request | Parámetros inválidos |
| 500 | Internal Server Error | Error en el orquestador o microservicios |

---

## Casos de Prueba Recomendados

### Caso 1: Servicio Funcionando Normalmente
✅ Todos los microservicios responden
✅ Datos consolidados se devuelven correctamente
✅ Rankings se calculan sin errores

### Caso 2: Un Microservicio Caído
- Detener MS2 (puerto 3000)
- Llamar a `/api/dashboard/consolidated`
- ✅ El orquestador debe continuar con MS1, MS3, MS4
- ✅ Metadata debe indicar que MS2 no respondió

### Caso 3: Usuario Sin Datos
- Llamar con `user_id=999` (usuario inexistente)
- ✅ Debe devolver estructuras vacías pero válidas
- ✅ No debe arrojar error

### Caso 4: Sin User ID
- Llamar sin parámetro `user_id`
- ✅ Debe devolver información global de todos los usuarios

---

## Herramientas Recomendadas

1. **Postman**: Para testing manual con interfaz gráfica
2. **Insomnia**: Alternativa ligera a Postman
3. **curl**: Para testing desde línea de comandos
4. **Swagger UI**: Incluido en http://localhost:8005/docs
5. **Python Script**: `tests/test_endpoints.py`

---

## Documentación Interactiva

Accede a la documentación interactiva en:

- **Swagger UI**: http://localhost:8005/docs
- **ReDoc**: http://localhost:8005/redoc

Desde ahí puedes:
- ✅ Ver todos los endpoints
- ✅ Probar endpoints directamente desde el navegador
- ✅ Ver esquemas de request/response
- ✅ Generar código de cliente automáticamente

---

## Troubleshooting

### Error: "Connection refused"
**Causa**: El microservicio no está corriendo
**Solución**: `python main.py`

### Error: "Service unavailable" en metadata
**Causa**: Uno o más microservicios backend no están disponibles
**Solución**: Verificar que MS1, MS2, MS3, MS4 estén corriendo

### Respuesta vacía en arrays
**Causa**: No hay datos en los microservicios backend
**Solución**: Verificar que los microservicios tengan datos de prueba

---

**Nota**: Asegúrate de que los microservicios 1-4 estén corriendo antes de probar el orquestador.
