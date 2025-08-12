
# 📚 Documentación - OneDrive Manager API

Este proyecto permite gestionar archivos y carpetas en una cuenta de OneDrive usando una API construida con FastAPI, integrando autenticación vía Microsoft Graph.

---

## 📁 Estructura del Proyecto

```
od_application/
│
├── app/                         # Código fuente principal de la app
│   ├── __init__.py
│   ├── main.py                  # Punto de entrada de FastAPI
│   ├── api_server.py            # Definición de rutas y endpoints
│   ├── auth/                    # Módulo de autenticación
│   │   ├── __init__.py
│   │   └── auth_manager.py
│   ├── od/                      # Lógica específica de OneDrive
│   │   ├── __init__.py
│   │   └── od_manager.py
│   ├── agents/                  # Agentes o clientes que consumen la API
│   │   ├── __init__.py
│   │   └── datacampus_agent.py
│   └── config.py                # Configuración global (usa dotenv)
│
├── tests/                       # Tests (unitarios o de integración)
│   ├── __init__.py
│   └── test_agent_debug.py
│
├── .env                         # Variables de entorno
├── .gitignore                   # Archivos a ignorar por git
├── README.md                    # Documentación del proyecto
├── requirements.txt             # Dependencias del entorno
```

---

## 🧠 Descripción de los Módulos

### 🔐 `auth_manager.py`
- Autenticación con Microsoft Graph API usando `msal`.
- Usa flujo de dispositivo (`device code flow`) para iniciar sesión.
- Cachea el token en disco para sesiones futuras.

### ☁️ `OD_manager.py`
- Abstracción de operaciones sobre OneDrive:
  - Crear/leer archivos Excel.
  - Listar carpetas.
  - Eliminar archivos.
  - Buscar elementos.
- Usa el token autenticado del `AuthManager`.

### 🌐 `api_server.py`
- Define la API REST con FastAPI.
- Expone endpoints como:
  - `/auth/login`
  - `/folders`
  - `/files/{id}/content`
  - `/files/excel`
  - `/items/{id}` (delete)
- Usa `Depends()` para controlar el acceso autenticado.

### ⚙️ `config.py`
- Centraliza la configuración cargando variables desde `.env`.
- Contiene los `SCOPES`, `AUTHORITY`, `CLIENT_ID`, `TENANT_ID`.

### 🧪 `test_agent_debug.py`
- Realiza pruebas automáticas de los endpoints y del agente.
- Permite verificar que el backend responde y autentica correctamente.

### 🤖 `datacampus_agent.py`
- Cliente HTTP que consume la API de `api_server.py`.
- Métodos disponibles:
  - `autenticar()`
  - `listar_contenido()`
  - `crear_reporte()`
  - `obtener_excel_como_json()`
  - `eliminar_elemento()`

### 🚀 `main.py`
- Punto de entrada del proyecto.
- Lanza el servidor FastAPI con Uvicorn:
  ```bash
  python main.py
  ```

---

## ⚙️ Requisitos

- Python 3.10 o superior.
- Credenciales válidas de Azure App Registrations (CLIENT_ID y TENANT_ID).
- Microsoft Graph habilitado para acceso a OneDrive personal o empresarial.

Instala los requisitos con:

```bash
pip install -r requirements.txt
```

---

## ▶️ Cómo ejecutar

### 1. Configura tu `.env`

```
CLIENT_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxx
TENANT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

### 2. Ejecuta el servidor:

```bash
cd OD_Application
python main.py
```

La API estará disponible en: [http://localhost:8000](http://localhost:8000)  
Documentación interactiva: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📌 Endpoints clave

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/auth/login` | Autenticación con OneDrive |
| `GET`  | `/folders` | Listar carpetas y archivos |
| `POST` | `/files/excel` | Crear archivo Excel |
| `GET`  | `/files/{id}/content` | Leer archivo como JSON |
| `PUT`  | `/files/{id}/content` | Actualizar archivo Excel |
| `DELETE` | `/items/{id}` | Eliminar archivo o carpeta |
| `POST` | `/files/upload` | Subir archivo `.xlsx` |
