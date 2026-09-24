from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from fastapi.staticfiles import StaticFiles
import os 
from app.layers.routers.pagos import router as pago_router

from app.db.session import engine
from app.layers.routers import (
    auth, tp_turismo, tp_servicio, gama, departamento, ciudad, 
    solicitud_proveedor, proveedor, documento, servicio,
    ubicacion, trayecto, detalle_resena, politica, condicion, servicio_imagen, servicio_condicion,
    servicio_gastronomia, servicio_recreacion, servicio_transporte, servicio_guia, plan_viaje
    
)

app = FastAPI(title="PAT API")

os.makedirs("app/static", exist_ok=True)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

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

app.include_router(auth.router)
app.include_router(tp_turismo.router)
app.include_router(tp_servicio.router)
app.include_router(gama.router)
app.include_router(departamento.router)
app.include_router(ciudad.router)
app.include_router(solicitud_proveedor.router)
app.include_router(proveedor.router)  
app.include_router(documento.router)
app.include_router(servicio.router)    
app.include_router(ubicacion.router)
app.include_router(trayecto.router)
app.include_router(detalle_resena.router)     
app.include_router(politica.router)
app.include_router(condicion.router)
app.include_router(servicio_imagen.router)    
app.include_router(servicio_condicion.router)
app.include_router(servicio_gastronomia.router)
app.include_router(servicio_recreacion.router)
app.include_router(servicio_transporte.router)
app.include_router(servicio_guia.router)
app.include_router(plan_viaje.router)
app.include_router(pago_router)




@app.get("/")
def root():
    return {"mensaje": "API del proyecto PAT funcionando correctamente."}