import geopandas as gpd
from shapely.geometry import Point
import pandas as pd
import numpy as np

path_zones = r'C:\Users\Usuario\Documents\proyectos\NYC_TAXIS\notebooks\geodata\taxi_zones.shp'
path_stations = r'C:\Users\Usuario\Documents\proyectos\NYC_TAXIS\notebooks\data_estaciones\coordenadas_estaciones.parquet'
radio_km = 2

# Cargar el archivo shapefile de las zonas en formato GeoDataFrame
zonas = gpd.read_file(path_zones)

# Cargar los datos de las estaciones desde el archivo parquet en formato DataFrame
estaciones = pd.read_parquet(path_stations)

# Convertir las coordenadas de las zonas y de las estaciones a EPSG:2263
zonas = zonas.to_crs(epsg=2263)
estaciones = gpd.GeoDataFrame(estaciones, geometry=gpd.points_from_xy(estaciones.Longitude, estaciones.Latitude), crs=4326)
estaciones = estaciones.to_crs(epsg=2263)

# Calcular el área de cada zona
zonas['area'] = zonas.geometry.area

# Calcular porcentaje de área de cada zona dentro de un círculo de 2 km centrado en cada estación
resultados = []

import warnings
warnings.filterwarnings('ignore', category=RuntimeWarning)
for index, row in estaciones.iterrows():
    # Crear un círculo con radio de 2 km centrado en la estación
    p = Point(row['geometry'].x, row['geometry'].y)
    circle = p.buffer(radio_km * 1000 * 3.281)

    # Calcular porcentaje de área dentro del círculo para cada zona
    zonas['porcentaje_area'] = np.where(zonas.geometry.intersects(circle),
                                        zonas.geometry.intersection(circle).area / zonas['area'] * 100, 0)

    # Almacenar los resultados en un DataFrame independiente y agregar la estación correspondiente
    porcentaje_areas = zonas[['OBJECTID', 'zone', 'porcentaje_area']].copy()
    porcentaje_areas['Station'] = row['Station']
    resultados.append(porcentaje_areas)

# Concatenar los resultados en un solo DataFrame
df_resultados = pd.concat(resultados, ignore_index=True)
df_resultados = df_resultados[['OBJECTID', 'zone', 'Station', 'porcentaje_area']]
df_resultados = df_resultados.replace([np.inf, -np.inf], np.nan).dropna()

xu = df_resultados[df_resultados['porcentaje_area'] > 50]
#xu.to_parquet('zonas_en_estaciones.parquet', index=False)

print(xu)