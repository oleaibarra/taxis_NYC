import os
import datetime
import boto3
import botocore
import requests
from funciones import generate_nyc_tlc_url, generate_object_key

# Constantes para la URL del sitio y la carpeta de destino en S3
SITE = os.environ.get('site')
BUCKET_NAME = os.environ.get('BUCKET_NAME')

def upload_to_aws(download_url, s3_key):
    # Crea un cliente de Amazon S3 usando la biblioteca `boto3`.
    s3 = boto3.client('s3')
    try:
        # Comprueba si el archivo ya existe en el bucket.
        s3.head_object(Bucket=BUCKET_NAME, Key=s3_key)
        print(f"File already exists in S3: {s3_key}")
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            # El archivo no existe en S3, continúa con la subida.
            try:
                response = requests.get(download_url, stream=True)
                response.raise_for_status()

                # Sube los datos a Amazon S3.
                s3.upload_fileobj(response.raw, BUCKET_NAME, s3_key)

                # Genera una URL de acceso prefirmado para el archivo subido.
                url = s3.generate_presigned_url(
                    ClientMethod='get_object',
                    Params={
                        'Bucket': BUCKET_NAME,
                        'Key': s3_key
                    },
                    ExpiresIn=24 * 3600
                )

                # Imprime un mensaje de éxito y devuelve la URL de acceso al archivo.
                print("Upload Successful", url)
                return url
            except Exception as e:
                # Si se produce un error al subir los datos a Amazon S3, imprime un mensaje de error y devuelve `None`.
                print("Error uploading to S3", e)
                return None
        else:
            # Hubo un error al intentar comprobar la existencia del archivo en S3.
            print("Error checking file existence in S3", e)
            return None


def lambda_handler(event, context):
    # Imprime un mensaje para indicar que se está comprobando el sitio web.
    print(f"Checking {SITE} at {event['time']}...")
    try:
        # Genera la URL de descarga del archivo a partir de la función `generate_nyc_tlc_url`.
        download_url = generate_nyc_tlc_url()
        print(f"Generated download URL: {download_url}")

        # Descarga el archivo y comprueba si la descarga fue exitosa.
        response = requests.get(download_url)
        if response.status_code == 200:
            print(f"Download URL is valid: {download_url}")
            # Genera la llave del objeto del archivo en Amazon S3 a partir de la función `generate_object_key`.
            s3_key = generate_object_key()
            # Sube el archivo a Amazon S3 usando la función `upload_to_aws`.
            upload_to_aws(download_url, s3_key)
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



