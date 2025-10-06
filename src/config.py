"""
Configuración de URLs y constantes para los microservicios.
"""

import os

# URLs base de los microservicios
# Se pueden configurar mediante variables de entorno para diferentes ambientes

MICROSERVICE1_URL = os.getenv("MICROSERVICE1_URL", "http://localhost:8081")
MICROSERVICE2_URL = os.getenv("MICROSERVICE2_URL", "http://localhost:3000")
MICROSERVICE3_URL = os.getenv("MICROSERVICE3_URL", "http://localhost:8000")
MICROSERVICE4_URL = os.getenv("MICROSERVICE4_URL", "http://localhost:8080")

# Endpoints específicos
ENDPOINTS = {
    "microservice1": {
        "users": f"{MICROSERVICE1_URL}/api/v1/auth/users",
        "profile": f"{MICROSERVICE1_URL}/api/v1/auth/profile",
    },
    "microservice2": {
        "scraped_accounts": f"{MICROSERVICE2_URL}/scrapedAccounts",
        "scraped_accounts_by_user": f"{MICROSERVICE2_URL}/scrapedAccounts/user",
        "questions": f"{MICROSERVICE2_URL}/questions",
    },
    "microservice3": {
        "dbquery_user": f"{MICROSERVICE3_URL}/dbquery/user",
        "dbquery_admin": f"{MICROSERVICE3_URL}/dbquery/admin",
    },
    "microservice4": {
        "dashboard": f"{MICROSERVICE4_URL}/getDashboardInfo",
    }
}

# Timeout para las peticiones HTTP (en segundos)
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))

# Configuración de reintentos
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
RETRY_DELAY = float(os.getenv("RETRY_DELAY", "1.0"))
