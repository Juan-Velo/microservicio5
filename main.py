"""
Microservicio 5 - Orquestador
==============================
Este microservicio actúa como orquestador que consume información de múltiples microservicios
y la consolida para el frontend, evitando que el frontend tenga que hacer múltiples llamadas.

Endpoints principales:
- GET / : Health check (status 200)
- GET /api/dashboard/consolidated : Información consolidada de todos los microservicios
- GET /api/dashboard/summary : Resumen y ranking de métricas principales
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from src.orchestrator_service import OrchestratorService
from src.models import ConsolidatedResponse, SummaryResponse

# Inicializar FastAPI
app = FastAPI(
    title="Microservicio 5 - Orquestador",
    description="Orquestador que consolida información de múltiples microservicios",
    version="1.0.0"
)

# Configurar CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar servicio de orquestación
orchestrator = OrchestratorService()


@app.get("/", tags=["Health Check"])
async def health_check():
    """
    Endpoint de verificación de salud del servicio.
    
    Returns:
        dict: Estado del servicio y timestamp
    """
    return {
        "status": "ok",
        "service": "Microservicio 5 - Orquestador",
        "version": "1.0.0",
        "message": "Service is running"
    }


@app.get("/api/dashboard/consolidated", response_model=ConsolidatedResponse, tags=["Orchestrator"])
async def get_consolidated_dashboard(user_id: int = None):
    """
    Endpoint principal de orquestación.
    
    Consume información de al menos 3 microservicios:
    - Microservicio 1: Información de usuarios
    - Microservicio 2: Cuentas scrapeadas
    - Microservicio 3: Métricas de queries
    - Microservicio 4: Información del dashboard
    
    Args:
        user_id (int, optional): ID del usuario para filtrar información específica
        
    Returns:
        ConsolidatedResponse: Información consolidada de todos los microservicios
        
    Example Response:
    {
        "users": [...],
        "scraped_accounts": [...],
        "metrics": {...},
        "dashboard_data": [...],
        "metadata": {
            "total_users": 10,
            "total_accounts": 25,
            "total_posts_analyzed": 150,
            "timestamp": "2025-10-05T12:00:00"
        }
    }
    """
    try:
        consolidated_data = await orchestrator.get_consolidated_data(user_id)
        return JSONResponse(content=consolidated_data, status_code=200)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al consolidar información: {str(e)}"
        )


@app.get("/api/dashboard/summary", response_model=SummaryResponse, tags=["Orchestrator"])
async def get_dashboard_summary(user_id: int = None):
    """
    Endpoint de resumen y ranking.
    
    Proporciona una vista resumida y rankings de la información consolidada:
    - Top usuarios más activos
    - Cuentas con mejores métricas
    - Resumen de engagement
    - Rankings globales
    
    Args:
        user_id (int, optional): ID del usuario para filtrar información específica
        
    Returns:
        SummaryResponse: Resumen y rankings de métricas principales
        
    Example Response:
    {
        "summary": {
            "total_users": 10,
            "total_accounts": 25,
            "average_engagement": 8.5,
            "total_views": 1000000
        },
        "rankings": {
            "top_users": [...],
            "top_accounts": [...],
            "best_engagement": [...]
        },
        "trends": {
            "growth_rate": 15.2,
            "engagement_trend": "increasing"
        },
        "timestamp": "2025-10-05T12:00:00"
    }
    """
    try:
        summary_data = await orchestrator.get_summary_data(user_id)
        return JSONResponse(content=summary_data, status_code=200)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al generar resumen: {str(e)}"
        )


@app.get("/api/health/services", tags=["Health Check"])
async def check_services_health():
    """
    Verifica el estado de conexión con todos los microservicios.
    
    Returns:
        dict: Estado de cada microservicio
    """
    try:
        health_status = await orchestrator.check_services_health()
        return JSONResponse(content=health_status, status_code=200)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al verificar servicios: {str(e)}"
        )


if __name__ == "__main__":
    # Configuración para desarrollo local
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8005,
        reload=True,
        log_level="info"
    )
