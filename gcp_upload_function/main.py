import datetime
import requests
from google.cloud import storage

# Constantes para la URL del sitio y la carpeta de destino en GCP
SITE = 'https://d37ci6vzurychx.cloudfront.net/trip-data'
BUCKET_NAME = 'nyc-taxis-raw'
taxis = ['green', 'yellow', 'fhvhv']


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

for taxi in taxis:
    def generate_nyc_tlc_url():
        # Genera la URL del archivo de datos a descargar en base al año y mes actual, y se guarda en la variable `url`.
        url = f"{SITE}/{taxi}_tripdata_{generate_data_year()}-{generate_data_month():02}.parquet"
        # Regresa la URL del archivo de datos.
        return url


    def generate_file_name():
        # Genera la llave del objeto del archivo de datos en Amazon S3 en base al año y mes actual, y se guarda en la variable `key`.
        key = f"{taxi}_tripdata_{generate_data_year()}-{generate_data_month():02}.parquet"
        # Regresa la llave del objeto del archivo de datos.
        return key
    def upload_to_gcp(download_url, nombre_archivo):
        # Crea un cliente de Google Cloud Storage.
        client = storage.Client()

        try:
            # Descarga los datos del archivo a la memoria usando la biblioteca `requests`.
            response = requests.get(download_url, stream=True)
            response.raise_for_status()

            # Obtiene el bucket de Google Cloud Storage donde se subirá el archivo.
            bucket = client.get_bucket(BUCKET_NAME)

            # Sube el archivo a Google Cloud Storage.
            blob = bucket.blob(nombre_archivo)
            blob.upload_from_string(response.content)

            # Genera una URL de acceso prefirmado para el archivo subido.
            url = blob.generate_signed_url(expiration=datetime.timedelta(days=1))

            # Imprime un mensaje de éxito y devuelve la URL de acceso al archivo.
            print("Upload Successful", url)
            return url
        except Exception as e:
            # Si se produce un error al subir los datos a Google Cloud Storage, imprime un mensaje de error y devuelve `None`.
            print("Error uploading to GCP", e)
            return None

    def process_file(event, _):
        # Imprime un mensaje para indicar que se está comprobando el sitio web.
        print(f"Checking {SITE} at {datetime.datetime.now()}...")
        try:
            # Genera la URL de descarga del archivo a partir de la función `generate_nyc_tlc_url`.
            download_url = generate_nyc_tlc_url()
            print(f"Generated download URL: {download_url}")

            # Descarga el archivo y comprueba si la descarga fue exitosa.
            response = requests.get(download_url)
            if response.status_code == 200:
                print(f"Download URL is valid: {download_url}")
                # Genera la llave del objeto del archivo en Google Cloud Storage a partir de la función `generate_object_key`.
                nombre_archivo = generate_file_name()
                # Sube el archivo a Google Cloud Storage usando la función `upload_to_gcp`.
                upload_to_gcp(download_url, nombre_archivo)
            else:
                print("URL not found. Will try again tomorrow.")

        except Exception as e:
            # Si se produce un error durante la comprobación, imprime un mensaje de error y lo relanza.
            print('Check failed!')
            print(e)
            raise
        else:
            # Si la comprobación es exitosa, imprime un mensaje de éxito y devuelve el tiempo actual.
            print('Check passed!')
            return event['time']
        finally:
            # Imprime un mensaje para indicar que se ha completado la comprobación.
            print(f'Check complete at {datetime.datetime.now()}')
