import requests
from geopy.distance import geodesic
from datetime import timedelta

def obtener_coordenadas(ciudad):
    overpass_url = "http://nominatim.openstreetmap.org/search"
    params = {
        'q': ciudad,
        'format': 'json'
    }
    response = requests.get(overpass_url, params=params)
    data = response.json()
    if data:
        return float(data[0]['lat']), float(data[0]['lon'])
    return None, None

def calcular_distancia_tiempo_combustible(ciudad_origen, ciudad_destino):
    lat_origen, lon_origen = obtener_coordenadas(ciudad_origen)
    lat_destino, lon_destino = obtener_coordenadas(ciudad_destino)
    if lat_origen is None or lon_origen is None or lat_destino is None or lon_destino is None:
        return None, None, None, None

    # Calcular la distancia en kilómetros
    distancia_km = geodesic((lat_origen, lon_origen), (lat_destino, lon_destino)).kilometers

    # Suponiendo un consumo de 10 km/litro, calcular el combustible requerido
    consumo_litros = distancia_km / 10

    # Suponiendo una velocidad promedio de 60 km/h, calcular la duración del viaje
    duracion_segundos = distancia_km / 60 * 3600
    duracion_timedelta = timedelta(seconds=duracion_segundos)
    horas = duracion_timedelta.seconds // 3600
    minutos = (duracion_timedelta.seconds % 3600) // 60
    segundos = duracion_timedelta.seconds % 60

    return distancia_km, horas, minutos, segundos, consumo_litros

# Solicitar ciudades de origen y destino
ciudad_origen = input('Ingrese la ciudad de origen: ')
ciudad_destino = input('Ingrese la ciudad de destino: ')

# Calcular la distancia, la duración del viaje y el combustible requerido
distancia_km, horas, minutos, segundos, consumo_litros = calcular_distancia_tiempo_combustible(ciudad_origen, ciudad_destino)

# Imprimir la narrativa del viaje
if distancia_km is not None and horas is not None and minutos is not None and segundos is not None and consumo_litros is not None:
    print(f'Distancia entre {ciudad_origen} y {ciudad_destino}: {distancia_km:.2f} km')
    print(f'Duración del viaje: {horas} horas, {minutos} minutos, {segundos} segundos')
    print(f'Combustible requerido: {consumo_litros:.2f} litros')
else:
    print('No se pudo encontrar la información de una de las ciudades.')
