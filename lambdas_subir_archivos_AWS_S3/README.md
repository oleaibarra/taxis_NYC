# La función Lambda para generar la carga automática de archivos a AWS S3

## En qué consiste el código que se escribió para la función lambda: 

El código es un programa de Python que tiene una función llamada lambda_handler, la cual es el manejador principal de una función Lambda de AWS. Esta función comprueba un sitio web para ver si hay un archivo disponible para descargar, y si es así, lo descarga y lo carga en Amazon S3. La función tiene las siguientes partes:

La función lambda_handler se define con dos argumentos, event y context, que son proporcionados por AWS al invocar la función. event es un diccionario que contiene información sobre el evento que desencadenó la invocación de la función Lambda, y context es un objeto que proporciona información sobre el entorno de ejecución de la función.

Dentro de lambda_handler, hay un bloque try-except-finally. El bloque try contiene las operaciones que se intentarán realizar y que pueden generar una excepción. Si se produce una excepción, el control se transfiere al bloque except para manejarla. La sección finally se ejecuta en cualquier caso, ya sea que se produzca una excepción o no.

En la sección try, se llama a la función generate_nyc_tlc_url para obtener la URL de descarga del archivo y se descarga el archivo usando la biblioteca requests. Si la descarga es exitosa, se genera la llave del objeto del archivo en Amazon S3 y se sube el archivo a Amazon S3 usando la función upload_to_aws.

Si se produce una excepción durante la descarga, subida o generación de la URL, se imprime un mensaje de error en la sección except, se relanza la excepción con raise y el control se transfiere al nivel superior en la pila de llamadas*.

Si la sección try se ejecuta sin excepciones, la sección else se ejecutará, que imprimirá un mensaje indicando que la comprobación fue exitosa y devolverá el tiempo actual.

En la sección finally, se imprime un mensaje que indica que se ha completado la comprobación y se muestra la hora actual.

Si no se puede hacer lo que se indica en try, el control se transfiere al bloque except. Si se puede hacer lo que se indica en try, se ejecuta la sección else antes de la sección finally. En cualquier caso, la sección finally siempre se ejecuta.

* La "pila de llamadas" (stack trace en inglés) es una estructura de datos utilizada por Python para rastrear las llamadas a funciones y los estados de las mismas. Cuando se produce una excepción en una función, Python detiene la ejecución de esa función y la remueve de la pila de llamadas. Entonces, Python busca si hay algún bloque try que pueda manejar la excepción. Si no se encuentra ningún bloque try que pueda manejar la excepción en la función actual, Python la relanza a la función que llamó a la función actual, y así sucesivamente.

En el código, si se produce una excepción durante la descarga, subida o generación de la URL, se relanza la excepción con raise. Esto significa que la excepción se propagará hacia el nivel superior en la pila de llamadas, es decir, la función que llamó a lambda_handler, o si la excepción ocurre en el nivel superior, se propagará hacia el entorno de ejecución de la función Lambda en AWS.

La implicación de esto es que la excepción se manejará adecuadamente en la función Lambda y se registrará para su posterior análisis. En otras palabras, si se produce un error durante la ejecución de la función Lambda, el entorno de ejecución en AWS detectará la excepción y registrará un registro de error, que puede ser utilizado para analizar y solucionar el problema.

### Para cargar este código a una función lambda a AWS se tiene que empaquetar en un archivo .zip de la siguiente manera: 

Estamos trabajando en el editor de pycharm y desde la terminal de powershell navegamos a la carpeta donde están nuestras funciones. 

```
folder_proyecto/
|-- lambda_function.py
|-- funciones.py
|-- requirements.txt
```
Como se observa, hay que crear previamente un archivo requirements.txt que contenga: 
```
boto3
requests
```
#### En powershell y en el direcotrio del proyecto craemos 'package'

```
mkdir package
```

#### Instalamos las bibliotecas necesarias en la carpeta package:

```
pip install -r requirements.txt -t package
```

#### Copiamos los archivos del proyecto en la carpeta package:

```
Copy-Item lambda_function.py, funciones.py -Destination package/
```

#### Comprimimos la carpeta package en un archivo zip:

```
Set-Location package
```
```
Compress-Archive -Path * -DestinationPath ..\package.zip
```
```
Set-Location ..
```


El codigo puede consultarse en lambda_function.py y en funciones.py incluídos en este repositorio.

## Creación de la función Lambda en AWS

1. Se crea un Bucket en AWS S3 donde se almacenarán los archivos que se suban. 
2. En el servicio Lambda de AWS damos a crear nueva función.
2.5. Seleccionamos Python 3.7 como lenguaje.
3. Le damos un nombre a la función y damos a crear. 
4. Después, en la nueva pantalla, bajamos un poco hasata ver la opción upload from, y seleccionamos upload a .zip file
5. Después de algo así como un minuto, terminará de cargar y desplegará un mensaje parecido a: 
```
The deployment package of your Lambda function "green_load" is too large to enable inline code editing. However, you can still invoke your function.(Todo arhivo que pese más de 10MB recibirá esta advertencia)
```
7. Justo encima de este mensaje hay un menú con opciones. Seleccionamos Configuration. 
8. En configuración hay más opciones de las que, en primer lugar, seleccionaremos Environment variables y dentro de esta opcion Edit. 
9. En edit creamos las siguientes variables (para nuestro caso específico y código específico): 
```
Key: BUCKET_NAME
Value: nyc-taxis-data
```
```
Key: site
Value: https://d37ci6vzurychx.cloudfront.net/trip-data
```
9. Damos en 'save' y nos regresa al menú de Configuration. 
10. En el menú seleccionamos 'Permission'. 
11. En pantalla nos mostrará un rol que se creó por default al crear la función lambda. Damos click en él.
12. Nos llevará a Identity and Access Management(IAM). 
13. Ahí seleccionaremos 'Add permissions' y después seleccionamos 'Attach policies'
14. Añadimos Amazons3fullaccess y damos click en 'add permission' (Si esta función la estará ejecutando alguien que no es el administrador de la cuenta, no es buena idea dar el fullaccess, pero no es nuestro caso y no encontramos una opción que fuera de write access. Quizá con s3:PutObject y s3:GetObject, pudiera funcionar).
15. De vuelta a nuestro módulo de lambda function. Seleccionamos la opción 'Add trigger'. 
16. Buscamos 'Event Bridge' y lo seleccionamos. 
17. Seleccionamos 'create new rule'.
18. Le damos un nombre a la regla y una explicación de lo que hace(puede ser el mismo nombre de nuevo).
19. En rule type dejamos seleccionado 'Schedule expression'
20. En Schedule expression escribimos, para nuestro caso que queremos que se dispare cada inicio de mes: 
```
cron(0 0 1 * ? *)
```
21. Ahora vamos a 'generalconfiguration' en el menú vertical (que se despliga al seleccionar 'Configuration' en el menú horizontal). 
22. Seleccionamos 'Edit' y en la opción 'timeout' modificamos para darle más tiempo (30 seg en nuestro caso). Y damos 'save'.
23. Para probar si la función nos regresará lo que queremos, vamos a probarla. 
24. En el menú horizontal, dos espacios a la izquierda de Configuration, se encuentra Test. Damos click. 
25. Creamos nuevo evento y le damos el nombre que querramos (por ejemplo: la-prueba-segundo-codigo). 
26. Para nuestro caso, como la función lambda_handler que escribimos toma parámetros time y event, debemos proporcionar la clave 'time' en el objeto event al invocar la función Lambda en la prueba. Lo hacemos utilizando el JSON template proporcionado al final de la página de pruebas modificando la información por: 
```
{
  "time": "2023-04-13T04:42:53.708Z"
}
```
25. Damos 'save'
26. Cuando nos diga que se grabó exitosamente, damos 'test'


