# AI Live Camera Atlas — Frontend

Frontend en Vite + React para el sistema de observación visual global.

## Qué muestra

- cámara principal con estilo premium
- ciudad, país y lugar exacto
- narrativa IA
- resumen global
- lista de canales
- auto-rotación
- voz del navegador con Speech Synthesis

## Instalación

```bash
npm install
npm run dev
```

## Variables de entorno

Copia `.env.example` a `.env`.

```bash
VITE_API_BASE_URL=https://tu-backend.onrender.com
VITE_ROTATION_SECONDS=30
```

## Endpoints esperados en el backend

- `GET /api/channels`
- `GET /api/channels/active`
- `GET /api/summary/global`
- `POST /api/rotate`
