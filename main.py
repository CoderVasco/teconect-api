from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import time
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from app.routes import auth, admin  # Importa a nova rota de administração

app = FastAPI()

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuração do Limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# Registro do handler de limite de taxa excedido
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Middleware de logging para monitorar requisições e respostas
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    logger.info(f"Response: status_code={response.status_code}, completed_in={process_time:.2f}s")

    return response

# Middleware para introduzir um atraso entre as requisições (se necessário)
@app.middleware("http")
async def throttle_requests(request: Request, call_next):
    response = await call_next(request)
    return response

# Inclui as rotas de autenticação e administração
app.include_router(auth.router)
app.include_router(admin.router)

@app.get("/")
@limiter.limit("5/minute")
async def read_root(request: Request):
    return {"message": "Welcome to Teconect API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
