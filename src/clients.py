"""
Clientes HTTP para consumir los diferentes microservicios.
Cada cliente encapsula la lógica de comunicación con un microservicio específico.
"""

import httpx
import asyncio
from typing import Dict, Any, List, Optional
from src.config import ENDPOINTS, REQUEST_TIMEOUT, MAX_RETRIES, RETRY_DELAY
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseClient:
    """Cliente base con funcionalidad común para todos los microservicios"""
    
    def __init__(self):
        self.timeout = REQUEST_TIMEOUT
        self.max_retries = MAX_RETRIES
        self.retry_delay = RETRY_DELAY
    
    async def _make_request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Realiza una petición HTTP con reintentos automáticos.
        
        Args:
            method: Método HTTP (GET, POST, etc.)
            url: URL del endpoint
            headers: Headers de la petición
            json_data: Datos JSON para POST
            params: Parámetros de query string
            
        Returns:
            Respuesta en formato dict o None si falla
        """
        for attempt in range(self.max_retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.request(
                        method=method,
                        url=url,
                        headers=headers,
                        json=json_data,
                        params=params
                    )
                    response.raise_for_status()
                    return response.json()
            except httpx.HTTPStatusError as e:
                logger.warning(f"HTTP error {e.response.status_code} en {url}: {e}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay)
                else:
                    logger.error(f"Falló después de {self.max_retries} intentos: {url}")
                    return None
            except Exception as e:
                logger.error(f"Error en petición a {url}: {str(e)}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay)
                else:
                    return None
        return None


class Microservice1Client(BaseClient):
    """Cliente para Microservicio 1 - Gestión de Usuarios"""
    
    async def get_all_users(self, token: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Obtiene todos los usuarios registrados.
        
        Args:
            token: Token de autenticación (requerido para este endpoint)
            
        Returns:
            Lista de usuarios
        """
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        url = ENDPOINTS["microservice1"]["users"]
        logger.info(f"Consultando usuarios en: {url}")
        
        response = await self._make_request("GET", url, headers=headers)
        return response if response else []
    
    async def get_user_profile(self, user_id: int, token: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Obtiene el perfil de un usuario específico.
        
        Args:
            user_id: ID del usuario
            token: Token de autenticación
            
        Returns:
            Información del perfil del usuario
        """
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        url = f"{ENDPOINTS['microservice1']['profile']}/{user_id}"
        logger.info(f"Consultando perfil de usuario {user_id} en: {url}")
        
        return await self._make_request("GET", url, headers=headers)


class Microservice2Client(BaseClient):
    """Cliente para Microservicio 2 - Cuentas Scrapeadas"""
    
    async def get_all_scraped_accounts(self, token: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Obtiene todas las cuentas scrapeadas.
        
        Args:
            token: Token de autenticación
            
        Returns:
            Lista de cuentas scrapeadas
        """
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        url = ENDPOINTS["microservice2"]["scraped_accounts"]
        logger.info(f"Consultando cuentas scrapeadas en: {url}")
        
        response = await self._make_request("GET", url, headers=headers)
        return response if response else []
    
    async def get_scraped_accounts_by_user(
        self,
        user_id: int,
        token: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Obtiene las cuentas scrapeadas de un usuario específico.
        
        Args:
            user_id: ID del usuario
            token: Token de autenticación
            
        Returns:
            Lista de cuentas scrapeadas del usuario
        """
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        url = f"{ENDPOINTS['microservice2']['scraped_accounts_by_user']}/{user_id}"
        logger.info(f"Consultando cuentas del usuario {user_id} en: {url}")
        
        response = await self._make_request("GET", url, headers=headers)
        return response if response else []
    
    async def get_all_questions(self, token: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Obtiene todas las preguntas/consultas del sistema.
        
        Args:
            token: Token de autenticación
            
        Returns:
            Lista de preguntas
        """
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        url = ENDPOINTS["microservice2"]["questions"]
        logger.info(f"Consultando preguntas en: {url}")
        
        response = await self._make_request("GET", url, headers=headers)
        return response if response else []


class Microservice3Client(BaseClient):
    """Cliente para Microservicio 3 - Métricas de TikTok"""
    
    async def query_user_metrics(
        self,
        user_id: Optional[int] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Consulta las métricas de TikTok para un usuario.
        
        Args:
            user_id: ID del usuario
            filters: Filtros adicionales para la query
            
        Returns:
            Métricas y dashboard del usuario
        """
        url = ENDPOINTS["microservice3"]["dbquery_user"]
        logger.info(f"Consultando métricas de usuario en: {url}")
        
        # Construir payload para la consulta
        payload = {}
        if user_id:
            payload["userId"] = user_id
        if filters:
            payload.update(filters)
        
        response = await self._make_request("POST", url, json_data=payload)
        return response if response else {"items": [], "count": 0, "dashboard": []}
    
    async def query_admin_metrics(
        self,
        admin_id: Optional[int] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Consulta las métricas de TikTok para un administrador.
        
        Args:
            admin_id: ID del administrador
            filters: Filtros adicionales para la query
            
        Returns:
            Métricas y dashboard del administrador
        """
        url = ENDPOINTS["microservice3"]["dbquery_admin"]
        logger.info(f"Consultando métricas de admin en: {url}")
        
        # Construir payload para la consulta
        payload = {}
        if admin_id:
            payload["adminId"] = admin_id
        if filters:
            payload.update(filters)
        
        response = await self._make_request("POST", url, json_data=payload)
        return response if response else {"items": [], "count": 0, "dashboard": []}


class Microservice4Client(BaseClient):
    """Cliente para Microservicio 4 - Dashboard Global"""
    
    async def get_dashboard_info(self) -> List[Dict[str, Any]]:
        """
        Obtiene información global del dashboard.
        
        Returns:
            Información del dashboard global
        """
        url = ENDPOINTS["microservice4"]["dashboard"]
        logger.info(f"Consultando dashboard global en: {url}")
        
        response = await self._make_request("GET", url)
        return response if response else []
