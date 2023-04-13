import os
import datetime
from urllib.request import Request, urlopen
from upload_to_aws import upload_to_aws  # Importa la función upload_to_aws desde upload_to_aws.py

SITE = os.environ['site']  # URL de la página de TLC Trip Record Data
def generate_nyc_tlc_url():
    current_date = datetime.datetime.now()
    if current_date.month > 3:
        previous_month = current_date.month - 3
        previous_month_year = current_date.year
    else:
        previous_month = current_date.month + 9
        previous_month_year = current_date.year - 1
    url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_{previous_month_year}-{previous_month:02}.parquet"
    return url

def generate_object_key():
    current_date = datetime.datetime.now()
    if current_date.month > 3:
        previous_month = current_date.month - 3
        previous_month_year = current_date.year
    else:
        previous_month = current_date.month + 9
        previous_month_year = current_date.year - 1
    llave_objeto = f"taxi/green_tripdata_{previous_month_year}-{previous_month:02}.parquet"
    return llave_objeto

def lambda_handler(event, context):
    print('Checking {} at {}...'.format(SITE, event['time']))
    try:
        download_url = generate_nyc_tlc_url()
        print(f"Generated download URL: {download_url}")

        req = Request(download_url, headers={'User-Agent': 'AWS Lambda'})
        response = urlopen(req)  # Intenta abrir la URL generada

        if response.status == 200:
            print(f"Download URL is valid: {download_url}")
            s3_file = generate_object_key()
            upload_to_aws(download_url, s3_file)  # Llama a la función upload_to_aws para cargar el archivo en S3
        else:
            print("URL not found. Will try again tomorrow.")

    except Exception as e:
        print('Check failed!')
        print(e)
        raise
    else:
        print('Check passed!')
        return event['time']
    finally:
        print('Check complete at {}'.format(str(datetime.datetime.now())))


