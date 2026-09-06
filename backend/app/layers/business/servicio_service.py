from fastapi import HTTPException, status
from sqlmodel import Session, select
from app.layers.data.servicio_repository import ServicioRepository
from app.layers.models.servicio import Servicio, ServicioHospedaje, HospedajeBaseCreate, HospedajeEspacioCreate, HospedajeBaseUpdate, HospedajeEspacioUpdate
from app.layers.models.auth import User
from app.layers.models.proveedor import Proveedor, ProveedorTpServicio
from app.layers.models.documento import Documento

class ServicioService:
    
    @staticmethod
    def validar_permisos_proveedor(db: Session, id_usu: int, id_tp_serv_requerido: int) -> Proveedor:
        proveedor = db.exec(select(Proveedor).where(Proveedor.id_usu == id_usu)).first()
        if not proveedor or proveedor.estado != "ACTIVO":
            raise HTTPException(status_code=403, detail="No eres un proveedor activo.")
        
        permiso = db.exec(select(ProveedorTpServicio).where(
            ProveedorTpServicio.id_prov == proveedor.id_prov, ProveedorTpServicio.id_tp_serv == id_tp_serv_requerido
        )).first()
        if not permiso:
            raise HTTPException(status_code=403, detail="No fuiste autorizado para ofrecer este tipo de servicio.")
            
        docs = db.exec(select(Documento).where(Documento.id_usu == id_usu)).all()
        if not docs:
            raise HTTPException(status_code=403, detail="Debes subir documentos legales antes de publicar servicios.")
            
        return proveedor

    # --- CREATE (POST) ---
    @staticmethod
    def crear_hotel_base(db: Session, data: HospedajeBaseCreate, usuario: User):
        prov = ServicioService.validar_permisos_proveedor(db, usuario.id_usu, 1) # 1 = Hospedaje
        
        nuevo_hotel = Servicio(
            nombre=data.nombre, descripcion=data.descripcion, id_tp_serv=1, 
            id_tp_turi=data.id_tp_turi, id_gama=data.id_gama, id_prov=prov.id_prov, id_ubi=data.id_ubi
        )
        hotel_guardado = ServicioRepository.crear_servicio_base(db, nuevo_hotel)
        return {"mensaje": "Hotel base creado.", "id_servicio": hotel_guardado.id_servicio}

    @staticmethod
    def agregar_espacio_hospedaje(db: Session, id_servicio: int, data: HospedajeEspacioCreate, usuario: User):
        prov = ServicioService.validar_permisos_proveedor(db, usuario.id_usu, 1)
        hotel = ServicioRepository.obtener_servicio_por_id(db, id_servicio)
        
        if not hotel or hotel.id_prov != prov.id_prov:
            raise HTTPException(status_code=404, detail="El alojamiento no existe o no te pertenece.")
            
        nuevo_espacio = ServicioHospedaje(
            id_servicio=id_servicio, nom_unidad=data.nom_unidad, capacidad_personas=data.capacidad_personas,
            vlr_noche=data.vlr_noche, horario_checkin=data.horario_checkin, horario_checkout=data.horario_checkout
        )
        espacio_guardado = ServicioRepository.agregar_espacio(db, nuevo_espacio)
        return {"mensaje": "Habitación agregada.", "id_hospedaje": espacio_guardado.id_hosp}
        
    # --- READ (GET) ---
    @staticmethod
    def listar_alojamientos_con_espacios(db: Session):
        hoteles = ServicioRepository.obtener_hoteles(db)
        respuesta = []
        for hotel in hoteles:
            espacios = ServicioRepository.obtener_espacios_de_hotel(db, hotel.id_servicio)
            respuesta.append({
                "id_servicio": hotel.id_servicio,
                "nombre": hotel.nombre,
                "descripcion": hotel.descripcion,
                "habitaciones_disponibles": espacios
            })
        return respuesta

    # --- UPDATE (PUT) ---
    @staticmethod
    def actualizar_hotel_base(db: Session, id_servicio: int, data: HospedajeBaseUpdate, usuario: User):
        prov = ServicioService.validar_permisos_proveedor(db, usuario.id_usu, 1)
        hotel = ServicioRepository.obtener_servicio_por_id(db, id_servicio)
        
        if not hotel or hotel.id_prov != prov.id_prov:
            raise HTTPException(status_code=404, detail="El hotel no existe o no te pertenece.")
            
        if data.nombre: hotel.nombre = data.nombre
        if data.descripcion: hotel.descripcion = data.descripcion
        if data.id_tp_turi: hotel.id_tp_turi = data.id_tp_turi
        if data.id_gama: hotel.id_gama = data.id_gama
        
        ServicioRepository.actualizar(db, hotel)
        return {"mensaje": "Información del hotel actualizada."}

    @staticmethod
    def actualizar_espacio(db: Session, id_hosp: int, data: HospedajeEspacioUpdate, usuario: User):
        prov = ServicioService.validar_permisos_proveedor(db, usuario.id_usu, 1)
        espacio = ServicioRepository.obtener_espacio_por_id(db, id_hosp)
        if not espacio:
            raise HTTPException(status_code=404, detail="Habitación no encontrada.")
            
        hotel = ServicioRepository.obtener_servicio_por_id(db, espacio.id_servicio)
        if hotel.id_prov != prov.id_prov:
            raise HTTPException(status_code=403, detail="Esta habitación pertenece a un hotel que no es tuyo.")
            
        if data.nom_unidad: espacio.nom_unidad = data.nom_unidad
        if data.capacidad_personas: espacio.capacidad_personas = data.capacidad_personas
        if data.vlr_noche: espacio.vlr_noche = data.vlr_noche
        if data.horario_checkin: espacio.horario_checkin = data.horario_checkin
        if data.horario_checkout: espacio.horario_checkout = data.horario_checkout
        
        ServicioRepository.actualizar(db, espacio)
        return {"mensaje": "Información de la habitación actualizada."}

    # --- DELETE (DELETE) ---
    @staticmethod
    def eliminar_hotel_base(db: Session, id_servicio: int, usuario: User):
        prov = ServicioService.validar_permisos_proveedor(db, usuario.id_usu, 1)
        hotel = ServicioRepository.obtener_servicio_por_id(db, id_servicio)
        
        if not hotel or hotel.id_prov != prov.id_prov:
            raise HTTPException(status_code=404, detail="El hotel no existe o no te pertenece.")
            
        hotel.activo = False # Borrado lógico para el hotel completo
        ServicioRepository.actualizar(db, hotel)
        return {"mensaje": "Hotel eliminado correctamente del sistema."}

    @staticmethod
    def eliminar_espacio(db: Session, id_hosp: int, usuario: User):
        prov = ServicioService.validar_permisos_proveedor(db, usuario.id_usu, 1)
        espacio = ServicioRepository.obtener_espacio_por_id(db, id_hosp)
        if not espacio:
            raise HTTPException(status_code=404, detail="Habitación no encontrada.")
            
        hotel = ServicioRepository.obtener_servicio_por_id(db, espacio.id_servicio)
        if hotel.id_prov != prov.id_prov:
            raise HTTPException(status_code=403, detail="No puedes borrar habitaciones de otros hoteles.")
            
        ServicioRepository.eliminar_espacio(db, espacio) # Borrado físico de la tabla hija
        return {"mensaje": "Habitación eliminada de tu hotel."}