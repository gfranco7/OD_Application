# Activar entorno virtual
& .\venv\Scripts\Activate.ps1

# Iniciar el servidor FastAPI
python -m uvicorn api_server:app --reload
