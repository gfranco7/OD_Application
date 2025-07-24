# test_agent_debug.py
from datacampus_agent import DatacampusAgent
import requests

def test_servidor_directo():
    """Prueba directa del servidor para comparar"""
    print("=== PRUEBA DIRECTA DEL SERVIDOR ===")
    try:
        # Prueba básica de conectividad
        response = requests.get("http://localhost:8000/")
        print(f"GET /: {response.status_code}")
        
        # Prueba de autenticación directa
        response = requests.post("http://localhost:8000/auth/login")
        print(f"POST /auth/login (sin datos): {response.status_code}")
        print(f"Response: {response.text}")
        
        response = requests.post("http://localhost:8000/auth/login", json={})
        print(f"POST /auth/login (JSON vacío): {response.status_code}")
        print(f"Response: {response.text}")
        
        headers = {'Content-Type': 'application/json'}
        response = requests.post("http://localhost:8000/auth/login", headers=headers, json={})
        print(f"POST /auth/login (con headers): {response.status_code}")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"Error en prueba directa: {e}")

def test_agente():
    """Prueba el agente"""
    print("\n=== PRUEBA DEL AGENTE ===")
    agent = DatacampusAgent()
    
    agent.debug_servidor()
    
    # Intentar autenticar
    print("\nIntentando autenticación...")
    if agent.autenticar():
        print("✓ Autenticación exitosa")
        
        # Probar otras funciones
        print("\nProbando listar contenido...")
        contenido = agent.listar_contenido()
        if contenido:
            print(f"✓ Contenido obtenido: {contenido}")
        else:
            print("✗ Error al obtener contenido")
            
    else:
        print("✗ Error en autenticación")

if __name__ == "__main__":
    test_servidor_directo()
    test_agente()