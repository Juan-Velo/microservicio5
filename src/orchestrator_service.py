"""
Servicio de orquestación que coordina las llamadas a múltiples microservicios
y consolida la información para el frontend.
"""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

from src.clients import (
    Microservice1Client,
    Microservice2Client,
    Microservice3Client,
    Microservice4Client
)
from src.models import (
    ConsolidatedMetadata,
    SummaryStats,
    Rankings,
    Trends
)

logger = logging.getLogger(__name__)


class OrchestratorService:
    """
    Servicio de orquestación que coordina las llamadas a múltiples microservicios.
    
    Este servicio:
    1. Realiza llamadas paralelas a los microservicios para optimizar el tiempo de respuesta
    2. Consolida la información recibida
    3. Calcula métricas agregadas y rankings
    4. Maneja errores de manera resiliente (si un servicio falla, los demás continúan)
    """
    
    def __init__(self):
        """Inicializa los clientes para cada microservicio"""
        self.ms1_client = Microservice1Client()
        self.ms2_client = Microservice2Client()
        self.ms3_client = Microservice3Client()
        self.ms4_client = Microservice4Client()
    
    async def get_consolidated_data(self, user_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Obtiene y consolida información de todos los microservicios.
        
        Este método realiza llamadas paralelas a:
        - Microservicio 1: Obtiene usuarios
        - Microservicio 2: Obtiene cuentas scrapeadas
        - Microservicio 3: Obtiene métricas de TikTok
        - Microservicio 4: Obtiene información del dashboard global
        
        Args:
            user_id: ID del usuario para filtrar información (opcional)
            
        Returns:
            Dict con toda la información consolidada y metadata
        """
        logger.info(f"Iniciando consolidación de datos para user_id={user_id}")
        
        # Realizar llamadas en paralelo para optimizar el tiempo de respuesta
        tasks = [
            self._get_users_data(user_id),
            self._get_scraped_accounts_data(user_id),
            self._get_metrics_data(user_id),
            self._get_dashboard_data()
        ]
        
        # Ejecutar todas las tareas en paralelo
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Procesar resultados (manejando excepciones individuales)
        users_data = results[0] if not isinstance(results[0], Exception) else []
        scraped_accounts_data = results[1] if not isinstance(results[1], Exception) else []
        metrics_data = results[2] if not isinstance(results[2], Exception) else {}
        dashboard_data = results[3] if not isinstance(results[3], Exception) else []
        
        # Construir metadata con información agregada
        metadata = self._build_metadata(
            users_data,
            scraped_accounts_data,
            metrics_data,
            dashboard_data
        )
        
        # Consolidar todo en una única respuesta
        consolidated = {
            "users": users_data,
            "scraped_accounts": scraped_accounts_data,
            "metrics": metrics_data,
            "dashboard_data": dashboard_data,
            "metadata": metadata
        }
        
        logger.info(f"Consolidación completada: {len(users_data)} usuarios, "
                   f"{len(scraped_accounts_data)} cuentas, "
                   f"{metrics_data.get('count', 0)} posts analizados")
        
        return consolidated
    
    async def get_summary_data(self, user_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Genera un resumen y rankings de la información consolidada.
        
        Proporciona:
        - Estadísticas resumidas (totales, promedios)
        - Rankings (top usuarios, mejores cuentas, mejor engagement)
        - Tendencias (crecimiento, engagement)
        
        Args:
            user_id: ID del usuario para filtrar información (opcional)
            
        Returns:
            Dict con resumen, rankings y tendencias
        """
        logger.info(f"Generando resumen para user_id={user_id}")
        
        # Obtener datos consolidados
        consolidated = await self.get_consolidated_data(user_id)
        
        # Calcular estadísticas resumidas
        summary = self._calculate_summary_stats(consolidated)
        
        # Calcular rankings
        rankings = self._calculate_rankings(consolidated)
        
        # Calcular tendencias
        trends = self._calculate_trends(consolidated)
        
        summary_response = {
            "summary": summary,
            "rankings": rankings,
            "trends": trends,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"Resumen generado con {len(rankings['top_users'])} top usuarios")
        
        return summary_response
    
    async def check_services_health(self) -> Dict[str, str]:
        """
        Verifica el estado de conexión con todos los microservicios de forma rápida.
        
        Returns:
            Dict con el estado de cada microservicio
        """
        logger.info("Verificando salud de servicios...")
        
        # Crear tareas paralelas para verificar todos los servicios simultáneamente con timeout
        tasks = [
            self._check_service_health("microservice1", self.ms1_client.get_all_users),
            self._check_service_health("microservice2", self.ms2_client.get_all_scraped_accounts),
            self._check_service_health("microservice3", self.ms3_client.query_user_metrics),
            self._check_service_health("microservice4", self.ms4_client.get_dashboard_info),
        ]
        
        # Ejecutar todas en paralelo con timeout de 5 segundos por servicio
        try:
            results = await asyncio.wait_for(
                asyncio.gather(*tasks, return_exceptions=True),
                timeout=5.0
            )
            
            # Construir respuesta con los resultados
            health_status = {}
            service_names = ["microservice1", "microservice2", "microservice3", "microservice4"]
            for i, result in enumerate(results):
                if isinstance(result, tuple):
                    health_status[result[0]] = result[1]
                else:
                    health_status[service_names[i]] = "timeout"
                    
        except asyncio.TimeoutError:
            logger.warning("Timeout al verificar salud de servicios")
            health_status = {
                "microservice1": "timeout",
                "microservice2": "timeout",
                "microservice3": "timeout",
                "microservice4": "timeout"
            }
        
        return health_status
    
    async def _check_service_health(self, service_name: str, check_func) -> tuple:
        """
        Verifica un servicio individual con timeout corto.
        
        Args:
            service_name: Nombre del servicio
            check_func: Función async para verificar el servicio
            
        Returns:
            Tuple (service_name, status)
        """
        try:
            # Intentar llamar al servicio con timeout de 2 segundos
            await asyncio.wait_for(check_func(), timeout=2.0)
            return (service_name, "healthy")
        except asyncio.TimeoutError:
            return (service_name, "timeout")
        except Exception as e:
            return (service_name, f"unhealthy: {str(e)[:50]}")
    
    # ================= Métodos privados auxiliares =================
    
    async def _get_users_data(self, user_id: Optional[int]) -> List[Dict[str, Any]]:
        """Obtiene datos de usuarios del microservicio 1"""
        try:
            if user_id:
                # Si se especifica un usuario, obtener solo ese perfil
                profile = await self.ms1_client.get_user_profile(user_id)
                return [profile] if profile else []
            else:
                # Obtener todos los usuarios
                return await self.ms1_client.get_all_users()
        except Exception as e:
            logger.error(f"Error obteniendo usuarios: {e}")
            return []
    
    async def _get_scraped_accounts_data(self, user_id: Optional[int]) -> List[Dict[str, Any]]:
        """Obtiene cuentas scrapeadas del microservicio 2"""
        try:
            if user_id:
                # Filtrar por usuario específico
                return await self.ms2_client.get_scraped_accounts_by_user(user_id)
            else:
                # Obtener todas las cuentas
                return await self.ms2_client.get_all_scraped_accounts()
        except Exception as e:
            logger.error(f"Error obteniendo cuentas scrapeadas: {e}")
            return []
    
    async def _get_metrics_data(self, user_id: Optional[int]) -> Dict[str, Any]:
        """Obtiene métricas del microservicio 3"""
        try:
            return await self.ms3_client.query_user_metrics(user_id)
        except Exception as e:
            logger.error(f"Error obteniendo métricas: {e}")
            return {"items": [], "count": 0, "dashboard": []}
    
    async def _get_dashboard_data(self) -> List[Dict[str, Any]]:
        """Obtiene datos del dashboard del microservicio 4"""
        try:
            return await self.ms4_client.get_dashboard_info()
        except Exception as e:
            logger.error(f"Error obteniendo dashboard: {e}")
            return []
    
    def _build_metadata(
        self,
        users: List,
        accounts: List,
        metrics: Dict,
        dashboard: List
    ) -> Dict[str, Any]:
        """Construye metadata con información agregada"""
        
        services_status = {
            "microservice1": "ok" if users else "no_data",
            "microservice2": "ok" if accounts else "no_data",
            "microservice3": "ok" if metrics.get("count", 0) > 0 else "no_data",
            "microservice4": "ok" if dashboard else "no_data"
        }
        
        return {
            "total_users": len(users),
            "total_accounts": len(accounts),
            "total_posts_analyzed": metrics.get("count", 0),
            "timestamp": datetime.now().isoformat(),
            "services_status": services_status
        }
    
    def _calculate_summary_stats(self, consolidated: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula estadísticas resumidas de los datos consolidados"""
        
        metrics = consolidated.get("metrics", {})
        items = metrics.get("items", [])
        dashboard = metrics.get("dashboard", [])
        
        # Calcular totales de métricas
        total_views = sum(item.get("views", 0) for item in items)
        total_likes = sum(item.get("likes", 0) for item in items)
        total_interactions = sum(item.get("totalInteractions", 0) for item in items)
        
        # Calcular promedio de engagement
        engagement_values = [item.get("engagement", 0) for item in items if item.get("engagement")]
        avg_engagement = sum(engagement_values) / len(engagement_values) if engagement_values else 0.0
        
        return {
            "total_users": consolidated["metadata"]["total_users"],
            "total_accounts": consolidated["metadata"]["total_accounts"],
            "average_engagement": round(avg_engagement, 2),
            "total_views": total_views,
            "total_likes": total_likes,
            "total_interactions": total_interactions
        }
    
    def _calculate_rankings(self, consolidated: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula rankings de usuarios y cuentas"""
        
        users = consolidated.get("users", [])
        accounts = consolidated.get("scraped_accounts", [])
        metrics = consolidated.get("metrics", {})
        items = metrics.get("items", [])
        
        # Top usuarios por número de cuentas scrapeadas
        user_account_count = {}
        for account in accounts:
            user_id = account.get("userId") or account.get("user_id")
            if user_id:
                user_account_count[user_id] = user_account_count.get(user_id, 0) + 1
        
        top_users = [
            {
                "user_id": user_id,
                "accounts_count": count,
                "email": next((u.get("email") for u in users if u.get("id") == user_id), "N/A")
            }
            for user_id, count in sorted(user_account_count.items(), key=lambda x: x[1], reverse=True)[:5]
        ]
        
        # Top cuentas por engagement
        account_metrics = {}
        for item in items:
            account = item.get("usernameTiktokAccount")
            if account:
                if account not in account_metrics:
                    account_metrics[account] = {
                        "account": account,
                        "total_views": 0,
                        "total_likes": 0,
                        "total_engagement": 0,
                        "post_count": 0
                    }
                account_metrics[account]["total_views"] += item.get("views", 0)
                account_metrics[account]["total_likes"] += item.get("likes", 0)
                account_metrics[account]["total_engagement"] += item.get("engagement", 0)
                account_metrics[account]["post_count"] += 1
        
        top_accounts = sorted(
            account_metrics.values(),
            key=lambda x: x["total_engagement"],
            reverse=True
        )[:5]
        
        # Posts con mejor engagement
        best_engagement = sorted(
            items,
            key=lambda x: x.get("engagement", 0),
            reverse=True
        )[:5]
        
        best_engagement_formatted = [
            {
                "post_id": post.get("postId"),
                "account": post.get("usernameTiktokAccount"),
                "engagement": post.get("engagement"),
                "views": post.get("views"),
                "likes": post.get("likes")
            }
            for post in best_engagement
        ]
        
        return {
            "top_users": top_users,
            "top_accounts": top_accounts,
            "best_engagement": best_engagement_formatted
        }
    
    def _calculate_trends(self, consolidated: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula tendencias de crecimiento y engagement"""
        
        metrics = consolidated.get("metrics", {})
        items = metrics.get("items", [])
        
        # Calcular tendencia de engagement (simplificado)
        if len(items) >= 2:
            # Ordenar por fecha
            sorted_items = sorted(
                items,
                key=lambda x: x.get("datePosted", ""),
                reverse=False
            )
            
            # Calcular engagement promedio de primera y segunda mitad
            mid = len(sorted_items) // 2
            first_half_eng = sum(i.get("engagement", 0) for i in sorted_items[:mid]) / mid if mid > 0 else 0
            second_half_eng = sum(i.get("engagement", 0) for i in sorted_items[mid:]) / (len(sorted_items) - mid) if (len(sorted_items) - mid) > 0 else 0
            
            # Determinar tendencia
            if second_half_eng > first_half_eng * 1.1:
                engagement_trend = "increasing"
            elif second_half_eng < first_half_eng * 0.9:
                engagement_trend = "decreasing"
            else:
                engagement_trend = "stable"
            
            # Calcular tasa de crecimiento
            growth_rate = ((second_half_eng - first_half_eng) / first_half_eng * 100) if first_half_eng > 0 else 0.0
        else:
            engagement_trend = "insufficient_data"
            growth_rate = 0.0
        
        return {
            "growth_rate": round(growth_rate, 2),
            "engagement_trend": engagement_trend
        }
