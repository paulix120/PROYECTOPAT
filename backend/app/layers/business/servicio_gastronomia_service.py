from typing import List, Dict, Any
from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.layers.data.servicio_gastronomia_repository import ServicioGastronomiaRepository
from app.layers.models.servicio import Servicio
from app.layers.models.servicio_gastronomia import (
    ServicioGastronomia, RestauranteBaseCreate, PlatoGastronomiaCreate,
    RestauranteBaseUpdate, PlatoGastronomiaUpdate,
)
from app.layers.models.auth import User
from app.layers.models.proveedor import Proveedor, ProveedorTpServicio
from app.layers.models.documento import Documento
from app.layers.models.tp_turismo import TpTurismo
from app.layers.models.gama import Gama
from app.layers.models.ubicacion import Ubicacion

class ServicioGastronomiaService:
    ID_TP_GASTRONOMIA = 2 

    @classmethod
    def validar_permisos_proveedor_gastronomia(cls, db: Session, id_usu: int) -> Proveedor:
        proveedor = db.exec(select(Proveedor).where(Proveedor.id_usu == id_usu)).first()
        if not proveedor or proveedor.estado != "ACTIVO":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No eres un proveedor activo en la plataforma.")

        permiso = db.exec(select(ProveedorTpServicio).where(
            ProveedorTpServicio.id_prov == proveedor.id_prov, ProveedorTpServicio.id_tp_serv == cls.ID_TP_GASTRONOMIA
        )).first()
        if not permiso:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No cuentas con autorización para ofrecer servicios gastronómicos.")

        docs = db.exec(select(Documento).where(Documento.id_usu == id_usu)).all()
        if not docs:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Debes cargar tus documentos legales antes de publicar.")

        return proveedor

    @classmethod
    def crear_restaurante_base(cls, db: Session, data: RestauranteBaseCreate, usuario: User) -> Dict[str, Any]:
        prov = cls.validar_permisos_proveedor_gastronomia(db, usuario.id_usu)
        if not db.get(TpTurismo, data.id_tp_turi) or not db.get(Gama, data.id_gama) or not db.get(Ubicacion, data.id_ubi):
             raise HTTPException(status_code=404, detail="El Tipo de turismo, Gama o Ubicación no existen.")

        nuevo_restaurante = Servicio(
            nombre=data.nombre.strip(), descripcion=data.descripcion.strip(), id_tp_serv=cls.ID_TP_GASTRONOMIA,
            id_tp_turi=data.id_tp_turi, id_gama=data.id_gama, id_prov=prov.id_prov, id_ubi=data.id_ubi
        )
        guardado = ServicioGastronomiaRepository.crear_restaurante_base(db, nuevo_restaurante)
        return {"mensaje": "Restaurante registrado con éxito.", "id_servicio": guardado.id_servicio, "nombre": guardado.nombre}

    @classmethod
    def agregar_plato_comida(cls, db: Session, id_servicio: int, data: PlatoGastronomiaCreate, usuario: User) -> Dict[str, Any]:
        prov = cls.validar_permisos_proveedor_gastronomia(db, usuario.id_usu)
        restaurante = ServicioGastronomiaRepository.obtener_restaurante_por_id(db, id_servicio)

        if not restaurante or restaurante.id_prov != prov.id_prov:
            raise HTTPException(status_code=404, detail="El restaurante no existe o no te pertenece.")

        nuevo_plato = ServicioGastronomia(
            id_servicio=id_servicio, nom_platillo_menu=data.nom_platillo_menu.strip(),
            porciones=data.porciones or 1, vlr_estimado=round(float(data.vlr_estimado), 2),
            horario_atencion=data.horario_atencion.strip() if data.horario_atencion else None
        )
        plato_guardado = ServicioGastronomiaRepository.agregar_plato(db, nuevo_plato)
        return {"mensaje": "Plato agregado exitosamente.", "id_gast": plato_guardado.id_gast}

    @classmethod
    def listar_restaurantes_con_menu(cls, db: Session) -> List[Dict[str, Any]]:
        restaurantes = ServicioGastronomiaRepository.obtener_restaurantes(db, solo_activos=True)
        resultado = []
        for r in restaurantes:
            platos = ServicioGastronomiaRepository.obtener_platos_de_restaurante(db, r.id_servicio)
            rest_dict = r.model_dump()
            rest_dict["menu_disponible"] = platos
            resultado.append(rest_dict)
        return resultado

    @classmethod
    def obtener_restaurante_por_id(cls, db: Session, id_servicio: int) -> Dict[str, Any]:
        restaurante = ServicioGastronomiaRepository.obtener_restaurante_por_id(db, id_servicio)
        if not restaurante or not restaurante.activo:
            raise HTTPException(status_code=404, detail="Restaurante no encontrado.")
        platos = ServicioGastronomiaRepository.obtener_platos_de_restaurante(db, id_servicio)
        rest_dict = restaurante.model_dump()
        rest_dict["menu_disponible"] = platos
        return rest_dict

    @classmethod
    def listar_mis_restaurantes(cls, db: Session, usuario: User) -> List[Dict[str, Any]]:
        prov = cls.validar_permisos_proveedor_gastronomia(db, usuario.id_usu)
        restaurantes = ServicioGastronomiaRepository.obtener_restaurantes_por_proveedor(db, prov.id_prov)
        resultado = []
        for r in restaurantes:
            platos = ServicioGastronomiaRepository.obtener_platos_de_restaurante(db, r.id_servicio)
            rest_dict = r.model_dump()
            rest_dict["menu_disponible"] = platos
            resultado.append(rest_dict)
        return resultado

    @classmethod
    def actualizar_restaurante_base(cls, db: Session, id_servicio: int, data: RestauranteBaseUpdate, usuario: User):
        prov = cls.validar_permisos_proveedor_gastronomia(db, usuario.id_usu)
        restaurante = ServicioGastronomiaRepository.obtener_restaurante_por_id(db, id_servicio)

        if not restaurante or restaurante.id_prov != prov.id_prov:
            raise HTTPException(status_code=404, detail="El restaurante no existe o no te pertenece.")

        if data.nombre: restaurante.nombre = data.nombre.strip()
        if data.descripcion: restaurante.descripcion = data.descripcion.strip()
        if data.id_tp_turi: restaurante.id_tp_turi = data.id_tp_turi
        if data.id_gama: restaurante.id_gama = data.id_gama
        if data.id_ubi: restaurante.id_ubi = data.id_ubi

        ServicioGastronomiaRepository.actualizar(db, restaurante)
        return {"mensaje": "Información del restaurante actualizada."}

    @classmethod
    def actualizar_plato(cls, db: Session, id_gast: int, data: PlatoGastronomiaUpdate, usuario: User):
        prov = cls.validar_permisos_proveedor_gastronomia(db, usuario.id_usu)
        plato = ServicioGastronomiaRepository.obtener_plato_por_id(db, id_gast)

        if not plato:
            raise HTTPException(status_code=404, detail="Platillo no encontrado.")

        restaurante = ServicioGastronomiaRepository.obtener_restaurante_por_id(db, plato.id_servicio)
        if not restaurante or restaurante.id_prov != prov.id_prov:
            raise HTTPException(status_code=403, detail="No tienes permisos para modificar este platillo.")

        if data.nom_platillo_menu: plato.nom_platillo_menu = data.nom_platillo_menu.strip()
        if data.porciones: plato.porciones = data.porciones
        if data.vlr_estimado: plato.vlr_estimado = round(float(data.vlr_estimado), 2)
        if data.horario_atencion: plato.horario_atencion = data.horario_atencion.strip()

        ServicioGastronomiaRepository.actualizar(db, plato)
        return {"mensaje": "Platillo actualizado exitosamente."}

    @classmethod
    def eliminar_restaurante_base(cls, db: Session, id_servicio: int, usuario: User):
        prov = cls.validar_permisos_proveedor_gastronomia(db, usuario.id_usu)
        restaurante = ServicioGastronomiaRepository.obtener_restaurante_por_id(db, id_servicio)

        if not restaurante or restaurante.id_prov != prov.id_prov:
            raise HTTPException(status_code=404, detail="El restaurante no existe o no te pertenece.")

        restaurante.activo = False
        ServicioGastronomiaRepository.actualizar(db, restaurante)
        return {"mensaje": f"Restaurante inactivado correctamente."}

    @classmethod
    def eliminar_plato(cls, db: Session, id_gast: int, usuario: User):
        prov = cls.validar_permisos_proveedor_gastronomia(db, usuario.id_usu)
        plato = ServicioGastronomiaRepository.obtener_plato_por_id(db, id_gast)

        if not plato:
            raise HTTPException(status_code=404, detail="Platillo no encontrado.")

        restaurante = ServicioGastronomiaRepository.obtener_restaurante_por_id(db, plato.id_servicio)
        if not restaurante or restaurante.id_prov != prov.id_prov:
            raise HTTPException(status_code=403, detail="No tienes autorización.")

        ServicioGastronomiaRepository.eliminar_plato(db, plato)
        return {"mensaje": "Platillo eliminado del menú exitosamente."}