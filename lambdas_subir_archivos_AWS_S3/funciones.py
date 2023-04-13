# Importa el módulo datetime que viene integrado en Python.
import datetime

# Asigna la URL del origen de datos a la variable SITE.
SITE = 'https://d37ci6vzurychx.cloudfront.net/trip-data'

# Asigna el nombre de la carpeta de destino en Amazon S3 a la variable S3_FOLDER.
S3_FOLDER = 'taxi/'

def generate_data_month():
    # Se obtiene la fecha y hora actuales y se guarda en la variable `current_date`.
    current_date = datetime.datetime.now()
    # Se calcula el mes de los datos que queremos recuperar en base al mes actual.
    # Si el mes actual es mayor que 3, se resta 3 del mes actual para obtener el mes deseado.
    # De lo contrario, se suma 9 al mes actual para obtener el mes deseado.
    data_month = current_date.month - 3 if current_date.month > 3 else current_date.month + 9
    # Regresa el mes deseado.
    return data_month

def generate_data_year():
    # Se obtiene la fecha y hora actuales y se guarda en la variable `current_date`.
    current_date = datetime.datetime.now()
    # Se calcula el año de los datos que queremos recuperar en base al mes actual.
    # Si el mes actual es mayor que 3, se usa el año actual como el año deseado.
    # De lo contrario, se resta 1 del año actual para obtener el año deseado.
    data_year = current_date.year if current_date.month > 3 else current_date.year - 1
    # Regresa el año deseado
    return data_year

def generate_nyc_tlc_url():
    # Genera la URL del archivo de datos a descargar en base al año y mes actual, y se guarda en la variable `url`.
    url = f"{SITE}/green_tripdata_{generate_data_year()}-{generate_data_month():02}.parquet"
    # Regresa la URL del archivo de datos.
    return url

def generate_object_key():
    # Genera la llave del objeto del archivo de datos en Amazon S3 en base al año y mes actual, y se guarda en la variable `key`.
    key = f"{S3_FOLDER}green_tripdata_{generate_data_year()}-{generate_data_month():02}.parquet"
    # Regresa la llave del objeto del archivo de datos.
    return key
