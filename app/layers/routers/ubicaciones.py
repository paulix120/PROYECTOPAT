from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.db.session import get_session
from app.layers.models.destinos import Departamento, Ciudad, TipoTurismo

router = APIRouter(prefix="/ubicaciones", tags=["Ubicaciones (Departamentos y Ciudades)"])

# --- DEPARTAMENTOS ---
@router.get("/departamentos", response_model=List[Departamento])
def listar_departamentos(db: Session = Depends(get_session)):
    return db.exec(select(Departamento)).all()

@router.post("/departamentos", response_model=Departamento, status_code=status.HTTP_201_CREATED)
def crear_departamento(nombre: str, db: Session = Depends(get_session)):
    nuevo_dep = Departamento(nombre=nombre)
    db.add(nuevo_dep)
    db.commit()
    db.refresh(nuevo_dep)
    return nuevo_dep

# --- CIUDADES ---
@router.get("/ciudades", response_model=List[Ciudad])
def listar_ciudades(db: Session = Depends(get_session)):
    return db.exec(select(Ciudad)).all()

@router.post("/ciudades", response_model=Ciudad, status_code=status.HTTP_201_CREATED)
def crear_ciudad(nombre: str, departamento_id: int, db: Session = Depends(get_session)):
    # Validar que el departamento existe
    dep_db = db.get(Departamento, departamento_id)
    if not dep_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El departamento especificado no existe."
        )
        
    nueva_ciudad = Ciudad(nombre=nombre, departamento_id=departamento_id)
    db.add(nueva_ciudad)
    db.commit()
    db.refresh(nueva_ciudad)
    return nueva_ciudad

@router.get("/tipos-turismo", response_model=List[TipoTurismo])
def listar_tipos_turismo(db: Session = Depends(get_session)):
    return db.exec(select(TipoTurismo)).all()

@router.post("/tipos-turismo", response_model=TipoTurismo, status_code=status.HTTP_201_CREATED)
def crear_tipo_turismo(nombre: str, descripcion: Optional[str] = None, db: Session = Depends(get_session)):
    nuevo_tipo = TipoTurismo(nombre=nombre, descripcion=descripcion)
    db.add(nuevo_tipo)
    db.commit()
    db.refresh(nuevo_tipo)
    return nuevo_tipo