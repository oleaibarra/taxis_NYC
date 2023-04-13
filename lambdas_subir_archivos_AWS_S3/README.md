
### Para crear nuestra función lambda para subir archivos a S3 

## Como primer paso hay que crear un bucket en AWS S3

## Trabajamos en la creación del código con Python 3.7

```
folder_proyecto/
|-- lambda_function.py
|-- funciones.py
|-- requirements.txt
```

### Navegamos al folder del proyecto en la terminal y creamos carpeta package (en este caso lo estamos haciendo desde powershell en pycharm)

```
mkdir package
```

### Instalamos las bibliotecas necesarias en la carpeta package:

```
pip install -r requirements.txt -t package
```

### Copiamos los archivos del proyecto en la carpeta package:

```
Copy-Item lambda_function.py, funciones.py -Destination package/
```

### Comprimimos la carpeta package en un archivo zip:

```
Set-Location package
```
```
Compress-Archive -Path * -DestinationPath ..\package.zip
```
```
Set-Location ..
```

### En AWS creamos función lambda
creamos rol y le asignamos permisos full para s3
en configuración añadimos variables de entorno: 
```
Key: BUCKET_NAME
Value: prueba-para-lambda-upload
```
```
Key: site
Value: https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page
```
### Para correr la prueba de testeo del lambda fuction hubo que modificar el json con: 
```
{
  "time": "2023-04-13T04:42:53.708Z"
}
```
#### La primera prueba falló por que tenía asignado muy poco tiempo de ejecución. 

En Configuracion; general; se subió el tiempo a 30 seg. y la prueba funcionó. 

Pero... 
Aunque se creó el objeto en el bucket, el objeto está vacío. Habrá que revisar de nuevo el código. 
