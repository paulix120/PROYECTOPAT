from sqlmodel import Session
from fastapi import HTTPException
from app.layers.data.base_repository import BaseRepository
from app.layers.models.auth import User
from app.layers.models.servicio import Servicio
from app.layers.business.servicio_service import ServicioService 
from app.layers.models.servicio_recreacion import ServicioRecreacion, RecreacionCreate, RecreacionUpdate
from app.layers.data.servicio_recreacion_repository import ServicioRecreacionRepository

class ServicioRecreacionService:
    @staticmethod
    def crear(db: Session, data: RecreacionCreate, usuario: User):
        prov_id = None
        if not data.es_evento_local:
            prov = ServicioService.validar_permisos_proveedor(db, usuario.id_usu, 3) 
            prov_id = prov.id_prov
            
        nuevo_padre = Servicio(nombre=data.nombre, descripcion=data.descripcion, id_tp_serv=3, id_tp_turi=data.id_tp_turi, id_gama=data.id_gama, id_prov=prov_id, id_ubi=data.id_ubi)
        padre_guardado = BaseRepository.guardar(db, nuevo_padre)
        
        nuevo_hijo = ServicioRecreacion(id_servicio=padre_guardado.id_servicio, nom_actividad=data.nom_actividad, duracion=data.duracion, horario=data.horario, vlr_persona=data.vlr_persona, capacidad=data.capacidad, es_evento_local=data.es_evento_local)
        BaseRepository.guardar(db, nuevo_hijo)
        return {"mensaje": "Recreación creada", "id_servicio": padre_guardado.id_servicio}

    @staticmethod
    def listar(db: Session):
        datos = ServicioRecreacionRepository.listar(db)
        return [{"servicio_base": p, "detalle": h} for p, h in datos]

    @staticmethod
    def actualizar(db: Session, id_servicio: int, data: RecreacionUpdate, usuario: User):
        padre = ServicioRecreacionRepository.obtener_padre(db, id_servicio)
        if not padre or padre.id_tp_serv != 3: raise HTTPException(404, "Servicio no encontrado.")
        if padre.id_prov:
            prov = ServicioService.validar_permisos_proveedor(db, usuario.id_usu, 3)
            if padre.id_prov != prov.id_prov: raise HTTPException(403, "No te pertenece.")

        hijo = ServicioRecreacionRepository.obtener_hijo(db, id_servicio)
        datos = data.model_dump(exclude_unset=True)
        for k in ["nombre", "descripcion", "id_tp_turi", "id_gama", "id_ubi"]:
            if k in datos: setattr(padre, k, datos[k])
        for k in ["nom_actividad", "duracion", "horario", "vlr_persona", "capacidad", "es_evento_local"]:
            if k in datos: setattr(hijo, k, datos[k])

        BaseRepository.actualizar(db, padre)
        BaseRepository.actualizar(db, hijo)
        return {"mensaje": "Recreación actualizada"}

    @staticmethod
    def eliminar(db: Session, id_servicio: int, usuario: User):
        padre = ServicioRecreacionRepository.obtener_padre(db, id_servicio)
        if not padre or padre.id_tp_serv != 3: raise HTTPException(404, "Servicio no encontrado.")
        if padre.id_prov:
            prov = ServicioService.validar_permisos_proveedor(db, usuario.id_usu, 3)
            if padre.id_prov != prov.id_prov: raise HTTPException(403, "No te pertenece.")
            
        padre.activo = False
        BaseRepository.actualizar(db, padre)
        return {"mensaje": "Recreación eliminada correctamente."}