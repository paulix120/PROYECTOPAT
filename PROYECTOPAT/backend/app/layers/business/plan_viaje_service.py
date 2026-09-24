from fastapi import HTTPException
from sqlmodel import Session
from decimal import Decimal
from app.layers.data.plan_viaje_repository import PlanViajeRepository
from app.layers.models.plan_viaje import PlanViaje, DetPlanViaje, PlanViajeCreate, ItemViajeCreate, PlanViajeUpdate, ItemViajeUpdate
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
        nuevo_plan = PlanViaje(
            nombre_plan=data.nombre_plan, 
            fecha_inicio=data.fecha_inicio, 
            fecha_fin=data.fecha_fin, 
            id_usu=usuario.id_usu,
            id_ubicacion_origen=data.id_ubicacion_origen,
            id_ubicacion_destino=data.id_ubicacion_destino
        )
        plan = PlanViajeRepository.crear_plan(db, nuevo_plan)
        return {"mensaje": "Plan de viaje creado", "id_plan_viaje": plan.id_plan_viaje}

    @staticmethod
    def agregar_item(db: Session, id_plan: int, data: ItemViajeCreate, usuario: User):
        plan = PlanViajeRepository.obtener_por_id(db, id_plan)
        if not plan or plan.id_usu != usuario.id_usu:
            raise HTTPException(404, "Plan de viaje no encontrado.")

        es_transporte = data.tipo_item in ("TRANSPORTE", "TRANSPORTE_PROPIO")

        if es_transporte:
            tiene_transporte = PlanViajeRepository.usuario_ya_tiene_transporte(db, usuario.id_usu)
            if tiene_transporte:
                raise HTTPException(
                    400,
                    "Ya tienes un transporte registrado en tus planes de viaje. "
                    "Solo puedes tener un transporte activo. Elimínalo si deseas agregar otro."
                )

        costo_unitario = Decimal("0.00")
        tiempo_minutos = 0
        id_ori_final = None
        id_des_final = None

        if data.tipo_item == 'TRANSPORTE_PROPIO':
            if not plan.id_ubicacion_origen or not plan.id_ubicacion_destino:
                raise HTTPException(400, "El plan de viaje no tiene origen y destino definidos. Por favor, vuelve a crear el plan o edítalo desde Mis Viajes.")
            origen = db.get(Ubicacion, plan.id_ubicacion_origen)
            destino = db.get(Ubicacion, plan.id_ubicacion_destino)
            distancia = calcular_distancia_km(origen.latitud, origen.longitud, destino.latitud, destino.longitud)
            costo_unitario = Decimal(str(distancia)) * Decimal("450.00")
            th = calcular_tiempo(distancia, velocidad_promedio=60)
            tiempo_minutos = int(th * 60) if th else 0
            id_ori_final = plan.id_ubicacion_origen
            id_des_final = plan.id_ubicacion_destino

        elif data.tipo_item == 'HOSPEDAJE':
            hosp = db.get(ServicioHospedaje, data.id_item_especifico)
            costo_unitario = Decimal(str(hosp.vlr_noche))
            
        elif data.tipo_item == 'GASTRONOMIA':
            plato = db.get(ServicioGastronomia, data.id_item_especifico)
            costo_unitario = Decimal(str(plato.vlr_estimado))
            
        elif data.tipo_item == 'TRANSPORTE': 
            ruta = db.get(ServicioTransporte, data.id_item_especifico)
            costo_unitario = Decimal(str(ruta.tarifa_base))
            
            if ruta.id_origen and ruta.id_destino:
                origen = db.get(Ubicacion, ruta.id_origen)
                destino = db.get(Ubicacion, ruta.id_destino)
                distancia = calcular_distancia_km(origen.latitud, origen.longitud, destino.latitud, destino.longitud)
                tipo_vehiculo = ruta.tipo_vehiculo.lower()
                velocidad = 800 if "avi" in tipo_vehiculo or "vuelo" in tipo_vehiculo or "airbus" in tipo_vehiculo else 60
                
                th = calcular_tiempo(distancia, velocidad_promedio=velocidad)
                tiempo_minutos = int(th * 60) if th else 0

                id_ori_final = ruta.id_origen
                id_des_final = ruta.id_destino
            
        elif data.tipo_item in ['DESTINO_TURISTICO', 'RECREACION', 'GUIA']:
            rec = db.get(ServicioRecreacion, data.id_item_especifico)
            if rec: costo_unitario = Decimal(str(rec.vlr_persona))
            tiempo_minutos = 180 
            
        subtotal = costo_unitario * Decimal(str(data.cantidad))

        nuevo_detalle = DetPlanViaje(
            id_plan_viaje=id_plan, id_servicio=data.id_servicio, tipo_item=data.tipo_item,
            id_item_especifico=data.id_item_especifico,
            id_ubicacion_origen=id_ori_final, id_ubicacion_destino=id_des_final,
            cantidad=data.cantidad, fecha_servicio=data.fecha_servicio,
            costo_unitario_calculado=costo_unitario, subtotal_calculado=subtotal,
            tiempo_estimado_min=tiempo_minutos, observaciones=data.observaciones
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

    @staticmethod
    def editar_plan(db: Session, id_plan: int, data: "PlanViajeUpdate", usuario: User):
        plan = PlanViajeRepository.obtener_por_id(db, id_plan)
        if not plan or plan.id_usu != usuario.id_usu:
            raise HTTPException(404, "Plan de viaje no encontrado.")
        if data.nombre_plan is not None: plan.nombre_plan = data.nombre_plan
        if data.fecha_inicio is not None: plan.fecha_inicio = data.fecha_inicio
        if data.fecha_fin is not None: plan.fecha_fin = data.fecha_fin
        if data.id_ubicacion_origen is not None: plan.id_ubicacion_origen = data.id_ubicacion_origen   
        if data.id_ubicacion_destino is not None: plan.id_ubicacion_destino = data.id_ubicacion_destino 
        PlanViajeRepository.actualizar_plan(db, plan)
        return {"mensaje": "Plan actualizado correctamente."}

    @staticmethod
    def eliminar_plan(db: Session, id_plan: int, usuario: User):
        plan = PlanViajeRepository.obtener_por_id(db, id_plan)
        if not plan or plan.id_usu != usuario.id_usu:
            raise HTTPException(404, "Plan de viaje no encontrado.")
        PlanViajeRepository.eliminar_plan(db, plan)
        return {"mensaje": "Plan eliminado correctamente."}

    @staticmethod
    def eliminar_item(db: Session, id_detalle: int, usuario: User):
        detalle = PlanViajeRepository.obtener_detalle_por_id(db, id_detalle)
        if not detalle:
            raise HTTPException(404, "Ítem no encontrado.")
        plan = PlanViajeRepository.obtener_por_id(db, detalle.id_plan_viaje)
        if not plan or plan.id_usu != usuario.id_usu:
            raise HTTPException(403, "No autorizado.")

        plan.costo_total_estimado -= detalle.subtotal_calculado
        if plan.costo_total_estimado < 0:
            plan.costo_total_estimado = Decimal("0.00")

        PlanViajeRepository.eliminar_detalle(db, detalle)
        PlanViajeRepository.actualizar_plan(db, plan)
        return {"mensaje": "Ítem eliminado del plan.", "NUEVO_TOTAL": plan.costo_total_estimado}

    @staticmethod
    def editar_item(db: Session, id_detalle: int, data: "ItemViajeUpdate", usuario: User):
        detalle = PlanViajeRepository.obtener_detalle_por_id(db, id_detalle)
        if not detalle:
            raise HTTPException(404, "Ítem no encontrado.")
        plan = PlanViajeRepository.obtener_por_id(db, detalle.id_plan_viaje)
        if not plan or plan.id_usu != usuario.id_usu:
            raise HTTPException(403, "No autorizado.")

        plan.costo_total_estimado -= detalle.subtotal_calculado

        if data.cantidad is not None:
            detalle.cantidad = data.cantidad
        if data.fecha_servicio is not None:
            detalle.fecha_servicio = data.fecha_servicio
        if data.personas is not None:
            base_obs = (detalle.observaciones or "").split(" | ")[0]
            detalle.observaciones = f"{base_obs} | {data.personas} persona(s)"

        nuevo_subtotal = detalle.costo_unitario_calculado * Decimal(str(detalle.cantidad))
        detalle.subtotal_calculado = nuevo_subtotal
        plan.costo_total_estimado += nuevo_subtotal

        PlanViajeRepository.actualizar_detalle(db, detalle)
        PlanViajeRepository.actualizar_plan(db, plan)
        return {"mensaje": "Ítem actualizado.", "nuevo_subtotal": nuevo_subtotal, "NUEVO_TOTAL": plan.costo_total_estimado}