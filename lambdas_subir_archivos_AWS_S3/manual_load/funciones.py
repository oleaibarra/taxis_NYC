# Importa el módulo datetime que viene integrado en Python.
import datetime
import os

# Constantes para la URL del sitio y la carpeta de destino en S3
SITE = os.environ.get('site')
green_yellow_fhvhv = os.environ.get('green_yellow_fhvhv')
month = os.environ.get('month_xx')
year = os.environ.get('year_xxxx')

# Asigna el nombre de la carpeta de destino en Amazon S3 a la variable S3_FOLDER.
S3_FOLDER = 'taxi/'
def generate_nyc_tlc_url():
    # Genera la URL del archivo de datos a descargar en base al año y mes actual, y se guarda en la variable `url`.
    url = f"{SITE}/{green_yellow_fhvhv}_tripdata_{year}-{month}.parquet"
    # Regresa la URL del archivo de datos.
    return url

def generate_object_key():
    # Genera la llave del objeto del archivo de datos en Amazon S3 en base al año y mes actual, y se guarda en la variable `key`.
    key = f"{S3_FOLDER}{green_yellow_fhvhv}_tripdata_{year}-{month}.parquet"
    # Regresa la llave del objeto del archivo de datos.
    return key
