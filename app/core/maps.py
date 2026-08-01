from geopy.geocoders import Nominatim
from typing import Tuple, Optional

geolocator = Nominatim(user_agent="pat_turismo_app")

def obtener_coordenadas_exactas(nombre: str, direccion: Optional[str], ciudad: str) -> Tuple[Optional[float], Optional[float]]:
    """
    Busca coordenadas exactas priorizando el NOMBRE del sitio turístico.
    """
    try:
        # Intento 1: Buscar por NOMBRE + CIUDAD (Ideal para parques, sitios emblemáticos, cerros)
        busqueda_nombre = f"{nombre}, {ciudad}, Colombia"
        location = geolocator.geocode(busqueda_nombre)

        # Intento 2: Si no encuentra por nombre y hay dirección, buscar por DIRECCIÓN + CIUDAD
        if not location and direccion:
            busqueda_direccion = f"{direccion}, {ciudad}, Colombia"
            location = geolocator.geocode(busqueda_direccion)

        if location:
            return round(location.latitude, 8), round(location.longitude, 8)

        return None, None
    except Exception as e:
        print(f"Error al consultar el servicio de mapas: {e}")
        return None, None