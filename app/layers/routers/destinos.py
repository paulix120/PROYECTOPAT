from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.db.session import get_session
from app.layers.models.destinos import (
    Destino, 
    DestinoResponse, 
    DestinoCreate, 
    DestinoUpdate,
    Ciudad
)
from app.core.maps import obtener_coordenadas_exactas

router = APIRouter(prefix="/destinos", tags=["Destinos Turísticos"])

# 1. GET: Listar TODOS los destinos 
@router.get("/", response_model=List[DestinoResponse])
def listar_destinos(db: Session = Depends(get_session)):
    query = select(Destino).where(Destino.activo == True)
    return db.exec(query).all()


# 2. GET: Obtener un destino por ID
@router.get("/{destino_id}", response_model=DestinoResponse)
def obtener_destino(
    destino_id: int,
    db: Session = Depends(get_session)
):
    destino = db.get(Destino, destino_id)
    if not destino or not destino.activo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El destino no existe o no está activo."
        )
    return destino


# 3. POST: Crear un nuevo destino
@router.post("/", response_model=DestinoResponse, status_code=status.HTTP_201_CREATED)
def crear_destino(
    data: DestinoCreate,
    db: Session = Depends(get_session)
):
    # 1. Buscar la ciudad en la BD para tener su nombre
    ciudad_db = db.get(Ciudad, data.ciudad_id)
    if not ciudad_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="La ciudad especificada no existe."
        )

    nuevo_destino = Destino.from_orm(data)

    if not nuevo_destino.latitud or nuevo_destino.latitud == 0:
        lat, lng = obtener_coordenadas_exactas(
            nombre=nuevo_destino.nombre, 
            direccion=nuevo_destino.direccion, 
            ciudad=ciudad_db.nombre
        )
        if lat and lng:
            nuevo_destino.latitud = lat
            nuevo_destino.longitud = lng

    db.add(nuevo_destino)
    db.commit()
    db.refresh(nuevo_destino)
    return nuevo_destino

# 4. PUT: Actualizar un destino existente
@router.put("/{destino_id}", response_model=DestinoResponse)
def actualizar_destino(
    destino_id: int,
    data: DestinoUpdate,
    db: Session = Depends(get_session)
):
    destino_db = db.get(Destino, destino_id)
    if not destino_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El destino que intentas actualizar no existe."
        )
    
    # Extraer solo los campos que el usuario envió en el JSON
    datos_nuevos = data.dict(exclude_unset=True)
    
    for clave, valor in datos_nuevos.items():
        setattr(destino_db, clave, valor)
        
    # Si cambió la ciudad, la buscamos para tener el nombre
    ciudad_nombre = ""
    if destino_db.ciudad_id:
        ciudad_db = db.get(Ciudad, destino_db.ciudad_id)
        if ciudad_db:
            ciudad_nombre = ciudad_db.nombre

    # Si actualizaron el nombre/dirección y NO enviaron coordenadas manuales, recalcular mapa
    if "latitud" not in datos_nuevos and "longitud" not in datos_nuevos:
        if "nombre" in datos_nuevos or "direccion" in datos_nuevos:
            lat, lng = obtener_coordenadas_exactas(
                nombre=destino_db.nombre,
                direccion=destino_db.direccion,
                ciudad=ciudad_nombre
            )
            if lat and lng:
                destino_db.latitud = lat
                destino_db.longitud = lng

    db.add(destino_db)
    db.commit()
    db.refresh(destino_db)
    return destino_db


# 5. DELETE: Eliminación lógica (Desactivar destino)
@router.delete("/{destino_id}")
def eliminar_destino(
    destino_id: int,
    db: Session = Depends(get_session)
):
    destino_db = db.get(Destino, destino_id)
    if not destino_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El destino no existe."
        )
    
    # Aplicamos borrado lógico recomendando buenas prácticas (se pasa activo a False)
    destino_db.activo = False
    db.add(destino_db)
    db.commit()
    
    return {"mensaje": f"El destino '{destino_db.nombre}' fue deshabilitado correctamente."}