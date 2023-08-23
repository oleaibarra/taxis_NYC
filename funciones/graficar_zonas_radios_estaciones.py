import geopandas as gpd
from shapely.geometry import Point
from matplotlib import pyplot as plt
from funciones.grados_a_cartesianas import grados_a_cartesianas
import pandas as pd

import os
os.environ['SHAPE_RESTORE_SHX'] = 'YES'
def graficar_zonas_cercanas(radio_km=2):

    # Cargar el archivo shapefile de las zonas
    zonas = gpd.read_file(r'C:\Users\Usuario\Documents\proyectos\NYC_TAXIS\notebooks\geodata\taxi_zones.shp')

    # La columna con valores únicos para cada zona es 'OBJECTID'

    # Crear un DataFrame con los puntos de las estaciones (coordenadas cartesianas)
    estaciones = grados_a_cartesianas(r'C:\Users\Usuario\Documents\proyectos\NYC_TAXIS\notebooks\data_estaciones\coordenadas_estaciones.parquet')

    # Crear una columna con los puntos en formato Point
    estaciones['geometry'] = estaciones.apply(lambda row: Point(row.x, row.y), axis=1)

    # Convertir radio de km a pies
    radio_pies = radio_km * 3280.84

    # Crear un DataFrame vacío para almacenar los resultados
    zonas_con_estaciones = gpd.GeoDataFrame()

    # Crear una figura
    fig, ax = plt.subplots(figsize=(7, 5))

    # Iterar sobre cada estación
    for i, estacion in estaciones.iterrows():
        # Crear un círculo de radio km alrededor del punto de la estación en pies
        circle = estacion['geometry'].buffer(radio_pies)

        # Crear un GeoDataFrame con el círculo
        circle_gdf = gpd.GeoDataFrame({'geometry': circle}, crs=zonas.crs, index=[0])

        # Realizar una intersección espacial entre el círculo y las zonas
        interseccion = gpd.overlay(zonas, circle_gdf, how='intersection')

        # Agregar la estación a la intersección
        interseccion['nombre_lugar'] = estacion['nombre_lugar']

        # Agregar la intersección a la lista de resultados
        zonas_con_estaciones = zonas_con_estaciones.append(interseccion)

        # Graficar el círculo
        circle_gdf.plot(ax=ax, color='red', alpha=0.9, legend=False)

    # Agregar un título al gráfico
    ax.set_title('Radios de medición de las estaciones de monitoreo')

    # Desactivar los ticks del eje x e y
    ax.set_xticks([])
    ax.set_yticks([])

    # Graficar las zonas, utilizando la columna 'id_zona' para asignar colores
    zonas.plot(ax=ax, column='OBJECTID', cmap='YlGnBu', alpha=0.2, edgecolor='black', linewidth=0.5, legend=False)

    # Graficar las estaciones
    estaciones.plot(ax=ax, color='black', markersize=50)

    # Ajustar los límites del gráfico
    ax.set_xlim(zonas.total_bounds[0] - radio_pies, zonas.total_bounds[2] + radio_pies)
    ax.set_ylim(zonas.total_bounds[1] - radio_pies, zonas.total_bounds[3] + radio_pies)

    # Mostrar el gráfico
    plt.show()



# Llamada a la función
graficar_zonas_cercanas(radio_km=2)
