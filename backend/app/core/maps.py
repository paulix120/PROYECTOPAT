from geopy.geocoders import Nominatim
from typing import Tuple, Optional
import time

geolocator = Nominatim(user_agent="pat_turismo_app")


def obtener_coordenadas_exactas(
    nombre: str,
    direccion: Optional[str],
    ciudad: str
) -> Tuple[Optional[float], Optional[float]]:

    """
    Busca las coordenadas de la forma más precisa posible.
    """

    consultas = []

    # 1. Nombre + Dirección + Ciudad
    if direccion:
        consultas.append(
            f"{nombre}, {direccion},  Colombia"
        )

    # 2. Dirección + Ciudad
    if direccion:
        consultas.append(
            f"{direccion}, Colombia"
        )

    # 3. Nombre + Ciudad
    consultas.append(
        f"{nombre},  Colombia"
    )

    # 4. Solo Dirección
    if direccion:
        consultas.append(
            f"{direccion}, Colombia"
        )

    # 5. Solo Nombre
    consultas.append(
        f"{nombre}, Colombia"
    )

    try:

        for consulta in consultas:

            location = geolocator.geocode(
                consulta,
                addressdetails=True
            )

            if location:

                return (
                    round(location.latitude, 8),
                    round(location.longitude, 8)
                )

            # OpenStreetMap recomienda no hacer consultas muy seguidas
            time.sleep(1)

        return None, None

    except Exception as e:

        print(
            f"Error obteniendo coordenadas: {e}"
        )

        return None, None