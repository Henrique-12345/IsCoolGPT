"""
IsCoolGPT - Assistente Inteligente para Estudantes
AplicaÃ§Ã£o FastAPI para auxiliar estudantes em suas disciplinas
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes import router
from app.core.config import settings

app = FastAPI(
    title="IsCoolGPT API",
    description="API do assistente inteligente para estudantes",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produÃ§Ã£o, especificar domÃ­nios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(router, prefix="/api/v1")


@app.get("/api")
async def api_root():
    """InformaÃ§Ãµes bÃ¡sicas sobre a API."""
    return {"message": "IsCoolGPT API", "version": "1.0.0", "docs": "/docs"}


@app.get("/health")
async def health_check():
    """Endpoint de health check para monitoramento."""
    return {"status": "healthy", "service": "iscoolgpt-api"}


# Servir frontend estÃ¡tico (HTML/CSS/JS)
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.ENVIRONMENT == "development",
    )
