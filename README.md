# AI Live Camera Atlas

Aplicación full-stack para observar cámaras públicas en varios canales, rotarlas cada 30 segundos y generar narrativa contextual con visión + LLM.

## Stack

- Frontend: React + Vite
- Backend: FastAPI
- Deploy: Render
- Formato de datos: JSON normalizado por canal/observación/resumen

## Estructura

- `frontend/`: UI principal
- `backend/`: API, memoria, rotación y adaptadores
- `shared/`: esquemas y constantes
- `scripts/`: utilidades
- `docs/`: arquitectura y despliegue

## Desarrollo local

### Backend
```bash
cd backend
python -m venv .venv
# activar entorno
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Variables de entorno

Copia los archivos `.env.example` y ajusta tus endpoints de visión y LLM cuando los tengas.

### Backend
- `FRONTEND_ORIGIN`
- `ROTATION_SECONDS`
- `VISION_PROVIDER`
- `LLM_PROVIDER`
- `VISION_API_URL`
- `LLM_API_URL`
- `VISION_API_KEY`
- `LLM_API_KEY`

### Frontend
- `VITE_API_BASE_URL`

## Deploy en Render

El archivo `render.yaml` define dos servicios:
- `api`: FastAPI
- `web`: Vite frontend

## Qué hace ahora

- lista varios canales
- rota automáticamente
- genera observación por canal
- mantiene resumen global
- expone endpoints listos para conectar visión real y LLM real

## Próximo paso

Conectar tus APIs reales al backend reemplazando los adaptadores `MockVisionProvider` y `MockLLMProvider`.


## Estado del proyecto

Listo para GitHub como base funcional con frontend, backend y despliegue.
