from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from app.db.session import engine

from app.layers.routers import auth


app = FastAPI(
    title="PAT API"
)


# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# INICIO
# ==========================================

@app.on_event("startup")
def on_startup():

    SQLModel.metadata.create_all(
        engine
    )


# ==========================================
# ROUTERS
# ==========================================

app.include_router(
    auth.router
)


# ==========================================
# ROOT
# ==========================================

@app.get("/")
def root():

    return {
        "mensaje": "API del proyecto PAT funcionando correctamente."
    }