"""
Modelos de datos para el microservicio orquestador.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class UserData(BaseModel):
    """Modelo para información de usuario"""
    id: Optional[int] = None
    email: Optional[str] = None
    role: Optional[str] = None
    created_at: Optional[str] = None


class ScrapedAccountData(BaseModel):
    """Modelo para cuenta scrapeada"""
    id: Optional[int] = None
    account_name: Optional[str] = None
    user_id: Optional[int] = None
    created_at: Optional[str] = None


class MetricsData(BaseModel):
    """Modelo para métricas de TikTok"""
    items: Optional[List[Dict[str, Any]]] = []
    count: Optional[int] = 0
    dashboard: Optional[List[Dict[str, Any]]] = []


class DashboardItem(BaseModel):
    """Modelo para item del dashboard"""
    data: Optional[Dict[str, Any]] = {}


class ConsolidatedMetadata(BaseModel):
    """Metadata de información consolidada"""
    total_users: int = 0
    total_accounts: int = 0
    total_posts_analyzed: int = 0
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    services_status: Dict[str, str] = {}


class ConsolidatedResponse(BaseModel):
    """Respuesta consolidada del endpoint principal"""
    users: List[Dict[str, Any]] = []
    scraped_accounts: List[Dict[str, Any]] = []
    metrics: Dict[str, Any] = {}
    dashboard_data: List[Dict[str, Any]] = []
    metadata: ConsolidatedMetadata


class SummaryStats(BaseModel):
    """Estadísticas resumidas"""
    total_users: int = 0
    total_accounts: int = 0
    average_engagement: float = 0.0
    total_views: int = 0
    total_likes: int = 0
    total_interactions: int = 0


class Rankings(BaseModel):
    """Rankings de métricas"""
    top_users: List[Dict[str, Any]] = []
    top_accounts: List[Dict[str, Any]] = []
    best_engagement: List[Dict[str, Any]] = []


class Trends(BaseModel):
    """Tendencias de métricas"""
    growth_rate: float = 0.0
    engagement_trend: str = "stable"


class SummaryResponse(BaseModel):
    """Respuesta del endpoint de resumen"""
    summary: SummaryStats
    rankings: Rankings
    trends: Trends
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
