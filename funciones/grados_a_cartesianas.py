import pandas as pd
import pyproj

def grados_a_cartesianas(path_archivo_parquet):
    '''
    Toma un archivo parquet con tres columnas: nombre_del_lugar, latitud, longitud con coordenadas en grados; y regresa un dataframe con columnas nombre_lugar, latitud, longitud convertidas a coordenadas cartesianas.
    '''

    # Definir el sistema de coordenadas origen (WGS 84 en este caso)
    crs_latlon = pyproj.CRS('EPSG:4326')

    # Definir el sistema de coordenadas destino (EPSG:2263)
    crs_proj = pyproj.CRS('EPSG:2263')

    # Leer el archivo parquet
    estaciones = pd.read_parquet(path_archivo_parquet)

    # Lista para almacenar los resultados
    estaciones_con_coordenadas = []

    for i, estacion in estaciones.iterrows():
        # Obtener el nombre de la estación
        nombre = estacion[0]

        # Obtener la latitud y longitud
        lat = estacion[1]
        lon = estacion[2]

        # Crear un transformador de coordenadas de CRS de latitud y longitud a CRS de proyección cartográfica
        transformer = pyproj.Transformer.from_crs(crs_latlon, crs_proj, always_xy=True)

        # Transformar las coordenadas origen a las coordenadas destino
        x, y = transformer.transform(lon, lat)

        # Agregar las coordenadas a la lista de resultados
        coordenadas = {'nombre_lugar': nombre, 'latitud': lat, 'longitud': lon, 'x': x, 'y': y}
        estaciones_con_coordenadas.append(coordenadas)

    # Crear un DataFrame a partir del diccionario
    df = pd.DataFrame(estaciones_con_coordenadas, columns=['nombre_lugar', 'latitud', 'longitud','x', 'y'])
    df.drop(['latitud', 'longitud'], axis=1, inplace=True)

    return df