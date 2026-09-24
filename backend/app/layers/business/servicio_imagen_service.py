import os
import shutil
from fastapi import UploadFile, HTTPException, status
from sqlmodel import Session
from app.layers.data.servicio_imagen_repository import ServicioImagenRepository
from app.layers.data.servicio_repository import ServicioRepository
from app.layers.models.servicio_imagen import ServicioImagen
from app.layers.models.auth import User
from app.layers.business.servicio_service import ServicioService

UPLOAD_DIR = "app/static/servicios"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class ServicioImagenService:
    @staticmethod
    def subir_imagen(db: Session, id_servicio: int, archivo: UploadFile, es_principal: bool, usuario_actual: User):
        servicio = ServicioRepository.obtener_servicio_por_id(db, id_servicio)
        if not servicio:
            raise HTTPException(status_code=404, detail="Este servicio no existe.")
            
        # Si NO es administrador (rol 2), verificamos que sea el proveedor dueño del servicio
        if usuario_actual.id_rol != 2:
            prov = ServicioService.validar_permisos_proveedor(db, usuario_actual.id_usu, servicio.id_tp_serv)
            if servicio.id_prov != prov.id_prov:
                raise HTTPException(status_code=403, detail="Este servicio no te pertenece.")

        ext = archivo.filename.split('.')[-1].lower()
        if ext not in ['jpg', 'jpeg', 'png', 'webp']:
            raise HTTPException(status_code=400, detail="Solo se permiten imágenes (JPG, PNG, WebP).")

        nombre_unico = f"srv_{id_servicio}_{archivo.filename}"
        ruta_fisica = os.path.join(UPLOAD_DIR, nombre_unico)
        with open(ruta_fisica, "wb") as buffer:
            shutil.copyfileobj(archivo.file, buffer)

        nueva_img = ServicioImagen(
            id_servicio=id_servicio,
            ruta_url=f"/static/servicios/{nombre_unico}",
            tipo_arch=ext,
            es_principal=es_principal
        )
        return ServicioImagenRepository.crear(db, nueva_img)

    @staticmethod
    def eliminar_imagen(db: Session, id_img: int, usuario_actual: User):
        imagen = ServicioImagenRepository.obtener_por_id(db, id_img)
        if not imagen:
            raise HTTPException(status_code=404, detail="Imagen no encontrada.")
            
        prov = ServicioService.validar_permisos_proveedor(db, usuario_actual.id_usu, 1)
        servicio = ServicioRepository.obtener_servicio_por_id(db, imagen.id_servicio)
        
        if not servicio or servicio.id_prov != prov.id_prov:
            raise HTTPException(status_code=403, detail="No puedes borrar imágenes de otros proveedores.")

        ServicioImagenRepository.eliminar(db, imagen)
        return {"mensaje": "Imagen eliminada exitosamente."}