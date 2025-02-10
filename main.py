from fastapi import FastAPI
# from backend.routers import headers_router
from routers import headers_router
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

#Añadir CORS
origins = [
    "http://localhost:3000",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)
app.include_router(headers_router.router)

