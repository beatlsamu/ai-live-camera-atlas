from __future__ import annotations
from fastapi import Header, HTTPException, status

async def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    # Placeholder for future authenticated endpoints.
    if x_api_key is not None and len(x_api_key) < 8:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
