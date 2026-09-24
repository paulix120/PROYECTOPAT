from sqlmodel import Session
from fastapi import HTTPException, status
from decimal import Decimal
from datetime import datetime
from app.layers.data.trayecto_repository import TrayectoRepository
from app.layers.models.trayecto import Trayecto, TrayectoCreate, TrayectoUpdate
from app.layers.models.ubicacion import Ubicacion
from app.core.travel import calcular_distancia_km, calcular_tiempo

class TrayectoService:
    @staticmethod
    def crear_trayecto(db: Session, data: TrayectoCreate):
        if data.id_origen == data.id_destino:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Origen y destino no pueden ser iguales.")

        origen = db.get(Ubicacion, data.id_origen)
        destino = db.get(Ubicacion, data.id_destino)

        if not origen or not destino:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ubicación de origen o destino no encontrada.")

        distancia = calcular_distancia_km(origen.latitud, origen.longitud, destino.latitud, destino.longitud)
        if distancia is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se pudo calcular la distancia.")

        tiempo_horas = calcular_tiempo(distancia_km=distancia, velocidad_promedio=60)
        tiempo_minutos = int(tiempo_horas * 60) if tiempo_horas else 0

        nuevo_trayecto = Trayecto(
            id_origen=data.id_origen, id_destino=data.id_destino,
            distancia_km=Decimal(str(distancia)), tiempo_estimado_min=tiempo_minutos
        )
        return TrayectoRepository.crear_o_actualizar(db, nuevo_trayecto)

    @staticmethod
    def listar_trayectos(db: Session):
        return TrayectoRepository.obtener_todos(db)

    @staticmethod
    def actualizar_trayecto(db: Session, id_tray: int, data: TrayectoUpdate):
        trayecto = TrayectoRepository.obtener_por_id(db, id_tray)
        if not trayecto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trayecto no encontrado.")

        nuevo_origen = data.id_origen or trayecto.id_origen
        nuevo_destino = data.id_destino or trayecto.id_destino

        if nuevo_origen == nuevo_destino:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Origen y destino no pueden ser iguales.")

        if data.id_origen or data.id_destino:
            origen_db = db.get(Ubicacion, nuevo_origen)
            destino_db = db.get(Ubicacion, nuevo_destino)
            
            distancia = calcular_distancia_km(origen_db.latitud, origen_db.longitud, destino_db.latitud, destino_db.longitud)
            tiempo_horas = calcular_tiempo(distancia_km=distancia, velocidad_promedio=60)

            trayecto.id_origen = nuevo_origen
            trayecto.id_destino = nuevo_destino
            trayecto.distancia_km = Decimal(str(distancia))
            trayecto.tiempo_estimado_min = int(tiempo_horas * 60) if tiempo_horas else 0
            trayecto.fecha_calculo = datetime.utcnow()

        return TrayectoRepository.crear_o_actualizar(db, trayecto)

    @staticmethod
    def eliminar_trayecto(db: Session, id_tray: int):
        trayecto = TrayectoRepository.obtener_por_id(db, id_tray)
        if not trayecto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trayecto no encontrado.")
        
        TrayectoRepository.eliminar_fisico(db, trayecto)
        return {"mensaje": "Trayecto eliminado con éxito."}