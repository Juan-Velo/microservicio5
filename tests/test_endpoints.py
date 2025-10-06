"""
Script de pruebas manuales para verificar el funcionamiento del orquestador.
Este script puede ejecutarse de forma independiente para probar los endpoints.
"""

import asyncio
import httpx
import json

BASE_URL = "http://localhost:8005"


async def test_health_check():
    """Prueba el endpoint de health check"""
    print("\n" + "="*60)
    print("TEST: Health Check")
    print("="*60)
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return response.status_code == 200
        except Exception as e:
            print(f"Error: {e}")
            return False


async def test_consolidated_dashboard():
    """Prueba el endpoint de dashboard consolidado"""
    print("\n" + "="*60)
    print("TEST: Dashboard Consolidado")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.get(f"{BASE_URL}/api/dashboard/consolidated")
            print(f"Status Code: {response.status_code}")
            data = response.json()
            
            # Mostrar resumen de la respuesta
            print(f"\nResumen de la respuesta:")
            print(f"  - Usuarios: {len(data.get('users', []))}")
            print(f"  - Cuentas Scrapeadas: {len(data.get('scraped_accounts', []))}")
            print(f"  - Posts Analizados: {data.get('metrics', {}).get('count', 0)}")
            print(f"  - Dashboard Items: {len(data.get('dashboard_data', []))}")
            print(f"\nMetadata:")
            print(f"  {json.dumps(data.get('metadata', {}), indent=2)}")
            
            return response.status_code == 200
        except Exception as e:
            print(f"Error: {e}")
            return False


async def test_consolidated_dashboard_with_user():
    """Prueba el endpoint de dashboard consolidado con filtro de usuario"""
    print("\n" + "="*60)
    print("TEST: Dashboard Consolidado (con user_id=1)")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.get(f"{BASE_URL}/api/dashboard/consolidated?user_id=1")
            print(f"Status Code: {response.status_code}")
            data = response.json()
            
            print(f"\nResumen de la respuesta:")
            print(f"  - Usuarios: {len(data.get('users', []))}")
            print(f"  - Cuentas Scrapeadas: {len(data.get('scraped_accounts', []))}")
            print(f"  - Posts Analizados: {data.get('metrics', {}).get('count', 0)}")
            
            return response.status_code == 200
        except Exception as e:
            print(f"Error: {e}")
            return False


async def test_summary():
    """Prueba el endpoint de resumen y rankings"""
    print("\n" + "="*60)
    print("TEST: Resumen y Rankings")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.get(f"{BASE_URL}/api/dashboard/summary")
            print(f"Status Code: {response.status_code}")
            data = response.json()
            
            print(f"\nResumen:")
            print(json.dumps(data.get('summary', {}), indent=2))
            
            print(f"\nTop 3 Usuarios:")
            for i, user in enumerate(data.get('rankings', {}).get('top_users', [])[:3], 1):
                print(f"  {i}. User ID: {user.get('user_id')}, "
                      f"Cuentas: {user.get('accounts_count')}, "
                      f"Email: {user.get('email')}")
            
            print(f"\nTop 3 Cuentas:")
            for i, account in enumerate(data.get('rankings', {}).get('top_accounts', [])[:3], 1):
                print(f"  {i}. {account.get('account')}, "
                      f"Views: {account.get('total_views'):,}, "
                      f"Engagement: {account.get('total_engagement')}")
            
            print(f"\nTendencias:")
            print(f"  - Tasa de crecimiento: {data.get('trends', {}).get('growth_rate')}%")
            print(f"  - Tendencia engagement: {data.get('trends', {}).get('engagement_trend')}")
            
            return response.status_code == 200
        except Exception as e:
            print(f"Error: {e}")
            return False


async def test_services_health():
    """Prueba el endpoint de estado de servicios"""
    print("\n" + "="*60)
    print("TEST: Estado de Servicios")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.get(f"{BASE_URL}/api/health/services")
            print(f"Status Code: {response.status_code}")
            data = response.json()
            
            print(f"\nEstado de microservicios:")
            for service, status in data.items():
                status_emoji = "✅" if status == "healthy" else "❌"
                print(f"  {status_emoji} {service}: {status}")
            
            return response.status_code == 200
        except Exception as e:
            print(f"Error: {e}")
            return False


async def run_all_tests():
    """Ejecuta todas las pruebas"""
    print("\n" + "="*60)
    print("INICIANDO PRUEBAS DEL MICROSERVICIO 5 - ORQUESTADOR")
    print("="*60)
    
    results = {
        "Health Check": await test_health_check(),
        "Dashboard Consolidado": await test_consolidated_dashboard(),
        "Dashboard Consolidado (filtrado)": await test_consolidated_dashboard_with_user(),
        "Resumen y Rankings": await test_summary(),
        "Estado de Servicios": await test_services_health()
    }
    
    print("\n" + "="*60)
    print("RESUMEN DE PRUEBAS")
    print("="*60)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    passed = sum(results.values())
    total = len(results)
    print(f"\nTotal: {passed}/{total} pruebas exitosas")
    print("="*60)


if __name__ == "__main__":
    print("Asegúrate de que el microservicio esté corriendo en http://localhost:8005")
    print("Para iniciar el servicio: python main.py")
    print("\nPresiona Enter para continuar...")
    input()
    
    asyncio.run(run_all_tests())
