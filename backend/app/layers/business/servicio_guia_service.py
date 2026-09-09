from sqlmodel import Session
from fastapi import HTTPException
from app.layers.data.base_repository import BaseRepository
from app.layers.models.auth import User
from app.layers.models.servicio import Servicio
from app.layers.business.servicio_service import ServicioService 
from app.layers.models.servicio_guia import ServicioGuia, GuiaCreate, GuiaUpdate
from app.layers.data.servicio_guia_repository import ServicioGuiaRepository

class ServicioGuiaService:
    @staticmethod
    def crear(db: Session, data: GuiaCreate, usuario: User):
        prov = ServicioService.validar_permisos_proveedor(db, usuario.id_usu, 5) 
        nuevo_padre = Servicio(nombre=data.nombre, descripcion=data.descripcion, id_tp_serv=5, id_tp_turi=data.id_tp_turi, id_gama=data.id_gama, id_prov=prov.id_prov, id_ubi=data.id_ubi)
        padre_guardado = BaseRepository.guardar(db, nuevo_padre)
        
        nuevo_hijo = ServicioGuia(id_servicio=padre_guardado.id_servicio, nombre_tour=data.nombre_tour, vlr_tour=data.vlr_tour, duracion_horas=data.duracion_horas, capacidad_grupo=data.capacidad_grupo, dificultad=data.dificultad, horario=data.horario)
        BaseRepository.guardar(db, nuevo_hijo)
        return {"mensaje": "Guía creado", "id_servicio": padre_guardado.id_servicio}

    @staticmethod
    def listar(db: Session):
        datos = ServicioGuiaRepository.listar(db)
        return [{"servicio_base": p, "detalle": h} for p, h in datos]

    @staticmethod
    def actualizar(db: Session, id_servicio: int, data: GuiaUpdate, usuario: User):
        padre = ServicioGuiaRepository.obtener_padre(db, id_servicio)
        if not padre or padre.id_tp_serv != 5: raise HTTPException(404, "Servicio no encontrado.")
        prov = ServicioService.validar_permisos_proveedor(db, usuario.id_usu, 5)
        if padre.id_prov != prov.id_prov: raise HTTPException(403, "No te pertenece.")

        hijo = ServicioGuiaRepository.obtener_hijo(db, id_servicio)
        datos = data.model_dump(exclude_unset=True)
        for k in ["nombre", "descripcion", "id_tp_turi", "id_gama", "id_ubi"]:
            if k in datos: setattr(padre, k, datos[k])
        for k in ["nombre_tour", "vlr_tour", "duracion_horas", "capacidad_grupo", "dificultad", "horario"]:
            if k in datos: setattr(hijo, k, datos[k])

        BaseRepository.actualizar(db, padre)
        BaseRepository.actualizar(db, hijo)
        return {"mensaje": "Guía actualizado"}

    @staticmethod
    def eliminar(db: Session, id_servicio: int, usuario: User):
        padre = ServicioGuiaRepository.obtener_padre(db, id_servicio)
        if not padre or padre.id_tp_serv != 5: raise HTTPException(404, "Servicio no encontrado.")
        prov = ServicioService.validar_permisos_proveedor(db, usuario.id_usu, 5)
        if padre.id_prov != prov.id_prov: raise HTTPException(403, "No te pertenece.")
            
        padre.activo = False
        BaseRepository.actualizar(db, padre)
        return {"mensaje": "Guía eliminado correctamente."}