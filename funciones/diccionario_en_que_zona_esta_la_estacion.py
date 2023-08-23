import geopandas as gpd
from shapely.geometry import Point
import pandas as pd
import math

path_zones = r'C:\Users\Usuario\Documents\proyectos\NYC_TAXIS\notebooks\geodata\taxi_zones.shp'
path_stations = r'C:\Users\Usuario\Documents\proyectos\NYC_TAXIS\notebooks\data_estaciones\coordenadas_estaciones.parquet'


def en_que_zona_esta_la_estacion(path_zones, path_stations):
    '''
    :param path_zones: un archivo shapefile con coordenadas cartesianas
    :param path_stations: un archivo parquet de tres columnas: nombre_lugar, latitud, longitud (en grados)
    :return: un diccionario con el nombre de la estación y la zona dónde se ubica.
    '''

    # Bloque 1. Carga de archivos

    # Cargar el archivo shapefile de las zonas en formato GeoDataFrame
    zonas = gpd.read_file(path_zones)

    # Cargar los datos de las estaciones desde el archivo parquet en formato DataFrame
    estaciones = pd.read_parquet(path_stations)

    # Convierte a grados las coordenadas cartesianas en zonas (coordenadas a EPSG:4326)
    zonas = zonas.to_crs(epsg=4326)


    # Bloque 2. Identificar las zonas donde están localizadas las estaciones

    # Crear un diccionario para almacenar la información de las estaciones
    diccionario_estaciones = {}

    # Iterar sobre cada estación
    for i, row in estaciones.iterrows():

        # Crear un objeto Point con las coordenadas de la estación
        punto_estacion = Point(row['Longitude'], row['Latitude'])

        # Iterar sobre cada zona para identificar en qué zona está la estación
        for j, row2 in zonas.iterrows():

            # Verificar si el punto de la estación está dentro de la geometría de la zona
            if punto_estacion.within(row2['geometry']):
                # Agregar la información de la zona al diccionario de la estación
                diccionario_estaciones[row['Station']] = {'OBJECTID': row2['OBJECTID'], 'zone': row2['zone']}

    # Imprimir el diccionario de estaciones
    return diccionario_estaciones


