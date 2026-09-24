from sqlmodel import Session
from fastapi import HTTPException, status
from decimal import Decimal
from app.layers.data.ubicacion_repository import UbicacionRepository
from app.layers.models.ubicacion import Ubicacion, UbicacionCreate, UbicacionUpdate
from app.layers.models.ciudad import Ciudad
from app.core.maps import obtener_coordenadas_exactas

class UbicacionService:
    @staticmethod
    def crear_ubicacion(db: Session, data: UbicacionCreate):
        ciudad = db.get(Ciudad, data.id_cdad)
        if not ciudad:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La ciudad no existe.")

        lat = data.latitud
        lon = data.longitud
        if lat is None or lon is None:
            lat_map, lon_map = obtener_coordenadas_exactas(
                nombre=data.barrio or data.direccion, 
                direccion=data.direccion, 
                ciudad=ciudad.nombre
            )
            if lat_map is None or lon_map is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se pudo calcular las coordenadas. Ingréselas manualmente.")
            lat, lon = Decimal(str(lat_map)), Decimal(str(lon_map))

        nueva_ubicacion = Ubicacion(
            direccion=data.direccion, barrio=data.barrio, codigo_postal=data.codigo_postal,
            latitud=lat, longitud=lon, descripcion=data.descripcion, id_cdad=data.id_cdad, activo=True
        )
        return UbicacionRepository.crear_o_actualizar(db, nueva_ubicacion)

    @staticmethod
    def listar_ubicaciones(db: Session):
        return UbicacionRepository.obtener_todas(db)

    @staticmethod
    def actualizar_ubicacion(db: Session, id_ubi: int, data: UbicacionUpdate):
        ubicacion = UbicacionRepository.obtener_por_id(db, id_ubi)
        if not ubicacion:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ubicación no encontrada.")
        
        datos = data.model_dump(exclude_unset=True)
        for key, value in datos.items():
            setattr(ubicacion, key, value)
            
        return UbicacionRepository.crear_o_actualizar(db, ubicacion)

    @staticmethod
    def eliminar_ubicacion(db: Session, id_ubi: int):
        ubicacion = UbicacionRepository.obtener_por_id(db, id_ubi)
        if not ubicacion:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ubicación no encontrada.")
        
        ubicacion.activo = False 
        UbicacionRepository.crear_o_actualizar(db, ubicacion)
        return {"mensaje": "Ubicación inactivada con éxito."}