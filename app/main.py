from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from app.db.session import engine

# Importamos todos los routers
from app.layers.routers import auth, destinos, ubicaciones, transporte

app = FastAPI(title="PAT API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

# Registrar Routers
app.include_router(auth.router)
app.include_router(destinos.router)
app.include_router(ubicaciones.router)
app.include_router(transporte.router) # <--- Agregamos el router de ubicaciones

@app.get("/")
def root():
    return {"mensaje": "API del proyecto PAT funcionando correctamente."}