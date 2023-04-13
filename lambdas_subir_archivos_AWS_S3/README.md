
### Para crear nuestra función lambda para subir archivos a S3 

## Como primer paso hay que crear un bucket en AWS S3

## Trabajamos en la creación del código con Python 3.7

```
folder_proyecto/
|-- lambda_function.py
|-- upload_to_aws.py
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
Copy-Item lambda_function.py, upload_to_aws.py -Destination package/
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

### Para correr la prueba de testeo del lambda fuction hubo que modificar el json con: 
```
{
  "time": "2023-04-13T04:42:53.708Z"
}
```

