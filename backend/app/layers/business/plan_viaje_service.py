from fastapi import HTTPException
from sqlmodel import Session
from decimal import Decimal
from app.layers.data.plan_viaje_repository import PlanViajeRepository
from app.layers.models.plan_viaje import PlanViaje, DetPlanViaje, PlanViajeCreate, ItemViajeCreate
from app.layers.models.auth import User
from app.layers.models.ubicacion import Ubicacion
from app.layers.models.servicio import ServicioHospedaje
from app.layers.models.servicio_gastronomia import ServicioGastronomia
from app.layers.models.servicio_transporte import ServicioTransporte
from app.layers.models.servicio_recreacion import ServicioRecreacion
from app.core.travel import calcular_distancia_km, calcular_tiempo

class PlanViajeService:
    @staticmethod
    def crear_plan(db: Session, data: PlanViajeCreate, usuario: User):
        if data.fecha_inicio > data.fecha_fin:
            raise HTTPException(400, "La fecha de inicio no puede ser posterior a la fecha de fin.")
        nuevo_plan = PlanViaje(nombre_plan=data.nombre_plan, fecha_inicio=data.fecha_inicio, fecha_fin=data.fecha_fin, id_usu=usuario.id_usu)
        plan = PlanViajeRepository.crear_plan(db, nuevo_plan)
        return {"mensaje": "Plan de viaje creado", "id_plan_viaje": plan.id_plan_viaje}

    @staticmethod
    def agregar_item(db: Session, id_plan: int, data: ItemViajeCreate, usuario: User):
        plan = PlanViajeRepository.obtener_por_id(db, id_plan)
        if not plan or plan.id_usu != usuario.id_usu:
            raise HTTPException(404, "Plan de viaje no encontrado.")

        costo_unitario = Decimal("0.00")
        tiempo_minutos = 0
        
        if data.tipo_item == 'TRANSPORTE_PROPIO':
            if not data.id_ubicacion_origen or not data.id_ubicacion_destino:
                raise HTTPException(400, "Falta origen y destino.")
            origen = db.get(Ubicacion, data.id_ubicacion_origen)
            destino = db.get(Ubicacion, data.id_ubicacion_destino)
            distancia = calcular_distancia_km(origen.latitud, origen.longitud, destino.latitud, destino.longitud)
            costo_unitario = Decimal(str(distancia)) * Decimal("450.00")
            th = calcular_tiempo(distancia, velocidad_promedio=60) # 60 km/h en carro
            tiempo_minutos = int(th * 60) if th else 0

        elif data.tipo_item == 'HOSPEDAJE':
            hosp = db.get(ServicioHospedaje, data.id_item_especifico)
            costo_unitario = Decimal(str(hosp.vlr_noche))
            
        elif data.tipo_item == 'GASTRONOMIA':
            plato = db.get(ServicioGastronomia, data.id_item_especifico)
            costo_unitario = Decimal(str(plato.vlr_estimado))
            
        elif data.tipo_item == 'TRANSPORTE': 
            ruta = db.get(ServicioTransporte, data.id_item_especifico)
            costo_unitario = Decimal(str(ruta.tarifa_base))
            
            # MAGIA: Detectar si es un VUELO (800 km/h) o un BUS (60 km/h)
            if ruta.id_origen and ruta.id_destino:
                origen = db.get(Ubicacion, ruta.id_origen)
                destino = db.get(Ubicacion, ruta.id_destino)
                distancia = calcular_distancia_km(origen.latitud, origen.longitud, destino.latitud, destino.longitud)
                
                tipo_vehiculo = ruta.tipo_vehiculo.lower()
                velocidad = 800 if "avi" in tipo_vehiculo or "vuelo" in tipo_vehiculo or "airbus" in tipo_vehiculo else 60
                
                th = calcular_tiempo(distancia, velocidad_promedio=velocidad)
                tiempo_minutos = int(th * 60) if th else 0
            
        elif data.tipo_item in ['DESTINO_TURISTICO', 'RECREACION', 'GUIA']:
            rec = db.get(ServicioRecreacion, data.id_item_especifico)
            if rec: costo_unitario = Decimal(str(rec.vlr_persona))
            tiempo_minutos = 180 
            
        subtotal = costo_unitario * Decimal(str(data.cantidad))

        nuevo_detalle = DetPlanViaje(
            id_plan_viaje=id_plan, id_servicio=data.id_servicio, tipo_item=data.tipo_item,
            id_item_especifico=data.id_item_especifico, cantidad=data.cantidad,
            fecha_servicio=data.fecha_servicio, costo_unitario_calculado=costo_unitario,
            subtotal_calculado=subtotal, tiempo_estimado_min=tiempo_minutos, observaciones=data.observaciones
        )
        PlanViajeRepository.agregar_detalle(db, nuevo_detalle)

        plan.costo_total_estimado += subtotal
        PlanViajeRepository.actualizar_plan(db, plan)

        return {"mensaje": f"{data.tipo_item} agregado", "subtotal": subtotal, "NUEVO_TOTAL": plan.costo_total_estimado}
        
    @staticmethod
    def obtener_mis_planes(db: Session, usuario: User):
        planes = PlanViajeRepository.obtener_por_usuario(db, usuario.id_usu)
        resultado = []
        for p in planes:
            detalles = PlanViajeRepository.obtener_detalles(db, p.id_plan_viaje)
            p_dict = p.model_dump()
            p_dict["items_agregados"] = detalles
            resultado.append(p_dict)
        return resultado