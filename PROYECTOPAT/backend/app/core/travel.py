from math import radians, sin, cos, sqrt, atan2
from decimal import Decimal
from typing import Optional

from app.core.maps import obtener_coordenadas_exactas


# ==========================================================
# RADIO DE LA TIERRA (Km)
# ==========================================================

RADIO_TIERRA = 6371


# ==========================================================
# OBTENER COORDENADAS DEL ORIGEN
# ==========================================================

def obtener_coordenadas_origen(
    origen: str
):
    """
    Convierte el origen escrito por el usuario
    en coordenadas geográficas.

    El usuario puede escribir una ciudad,
    una dirección o un lugar específico.
    """

    return obtener_coordenadas_exactas(
        nombre=origen,
        direccion=None,
        ciudad=""
    )


# ==========================================================
# CALCULAR DISTANCIA
# ==========================================================

def calcular_distancia_km(

    lat1,
    lon1,
    lat2,
    lon2

):

    """
    Distancia entre dos puntos usando Haversine.
    """

    if None in [lat1, lon1, lat2, lon2]:
        return None

    lat1 = radians(float(lat1))
    lon1 = radians(float(lon1))

    lat2 = radians(float(lat2))
    lon2 = radians(float(lon2))

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (

        sin(dlat / 2) ** 2

        +

        cos(lat1)

        *

        cos(lat2)

        *

        sin(dlon / 2) ** 2

    )

    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )

    distancia = RADIO_TIERRA * c

    return round(
        distancia,
        2
    )


# ==========================================================
# TIEMPO ESTIMADO
# ==========================================================

def calcular_tiempo(

    distancia_km,
    velocidad_promedio

):

    if distancia_km is None:
        return None

    if velocidad_promedio <= 0:
        return None

    horas = distancia_km / velocidad_promedio

    return round(
        horas,
        2
    )


# ==========================================================
# COSTO DEL TRANSPORTE
# ==========================================================

def calcular_costo_transporte(

    distancia_km,

    costo_km

):

    if distancia_km is None:
        return None

    if costo_km is None:
        return None

    total = Decimal(
        str(distancia_km)
    ) * Decimal(
        str(costo_km)
    )

    return total.quantize(
        Decimal("0.01")
    )