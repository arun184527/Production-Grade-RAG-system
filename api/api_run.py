from pyngrok import ngrok

# Start FastAPI server
!uvicorn api.app:app --host 0.0.0.0 --port 8000 &