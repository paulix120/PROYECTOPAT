from functools import lru_cache
import logging
import threading
import time
from typing import Optional, Tuple
from geopy.geocoders import Nominatim

logger = logging.getLogger(__name__)

geolocator = Nominatim(user_agent="pat_turismo_app", timeout=5)

_rate_lock = threading.Lock()
_ultima_consulta_ts = 0.0


def _respetar_rate_limit(intervalo_seg: float = 1.0) -> None:
    """Respeta el límite de 1 petición/segundo de Nominatim solo si hubo otra petición real reciente."""
    global _ultima_consulta_ts
    with _rate_lock:
        ahora = time.monotonic()
        transcurrido = ahora - _ultima_consulta_ts
        if _ultima_consulta_ts > 0 and transcurrido < intervalo_seg:
            time.sleep(intervalo_seg - transcurrido)
        _ultima_consulta_ts = time.monotonic()


def _construir_consultas(nombre: str, direccion: Optional[str], ciudad: str) -> list[str]:
    partes_base = []
    nom = (nombre or "").strip()
    dir_ = (direccion or "").strip()
    ciu = (ciudad or "").strip()

    if nom and dir_ and ciu:
        partes_base.append(f"{nom}, {dir_}, {ciu}, Colombia")
    if dir_ and ciu:
        partes_base.append(f"{dir_}, {ciu}, Colombia")
    if nom and ciu:
        partes_base.append(f"{nom}, {ciu}, Colombia")
    if dir_:
        partes_base.append(f"{dir_}, Colombia")
    if nom:
        partes_base.append(f"{nom}, Colombia")

    # Eliminar duplicados preservando el orden de prioridad
    return list(dict.fromkeys(partes_base))


@lru_cache(maxsize=512)
def _buscar_en_cache(nombre_norm: str, direccion_norm: str, ciudad_norm: str) -> Tuple[Optional[float], Optional[float]]:
    consultas = _construir_consultas(nombre_norm, direccion_norm or None, ciudad_norm)

    for consulta in consultas:
        try:
            _respetar_rate_limit(1.0)
            location = geolocator.geocode(consulta, addressdetails=True, country_codes="co")
            if location:
                return (round(location.latitude, 8), round(location.longitude, 8))
        except Exception as e:
            logger.warning("Error geocodificando '%s': %s", consulta, e)

    return None, None


def obtener_coordenadas_exactas(
    nombre: str,
    direccion: Optional[str],
    ciudad: str
) -> Tuple[Optional[float], Optional[float]]:
    """
    Busca las coordenadas de la forma más precisa posible usando caché en memoria.
    """
    nom_norm = (nombre or "").strip().lower()
    dir_norm = (direccion or "").strip().lower()
    ciu_norm = (ciudad or "").strip().lower()

    if not nom_norm and not dir_norm:
        return None, None

    coords = _buscar_en_cache(nom_norm, dir_norm, ciu_norm)

    # No memorizar fallos temporales de red/servicio si devolvió (None, None)
    if coords == (None, None):
        _buscar_en_cache.cache_clear()

    return coords