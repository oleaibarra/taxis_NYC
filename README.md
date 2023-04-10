# taxis_NYC
NYC Taxis Data Science Project 

## Análisis preliminar de calidad de datos

### Información sobre los movimientos de los taxis en la ciudad de Nueva York

La base para el estudio será la información descargable en el sitio de “NYC Taxi & Limousine Commission (TLC)”: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

Para el análisis preliminar del movimiento de taxis en la ciudad de Nueva York se utilizarán los archivos parquet que se pueden descargar por año/mes para cada tipo de servicio: 

•	Yellow Taxi Trip Records   
•	Green Taxi Trip Records   
•	For-Hire Vehicle Trip Records   
•	High Volume For-Hire Vehicle Trip Records   

Estos archivos contienen, entre otros, datos respecto a la fecha y hora de inicio y fin del servicio, distancia recorrida, punto de inicio y fin codificada por zonas definidas por la TLC y que pueden ser consultadas en el archivo:

•	Taxi Zone Lookup Table (CSV)

Así como en el siguiente shape file:  
•	Taxi Zone Shapefile (PARQUET)

Un análisis descriptivo de la información de los FHV-HV para el mes de enero de 2023 se encuentra en el notebook:

• 'VFH_HV_analisis_descriptivo.ipynb' 

y en formato PDF en:

• 'FHV_HV_analisis_descriptivo.pdf'

La información para los taxis amarillos (yellow) es prácticamente la misma que para los vehículos For Hire con alta demanda (HV), con exepción que para los amarillos existe el campo total_amount que contiene el total que tendrá que ser calculado para los VFH_HV sumando los campos base_passenger_fare, tolls, bcf, sales_tax, congestion_surcharge y tips. 

Por otro lado el archivo de los taxis amarillos no cuenta con la duración del viaje (trip_time) presente el archivo de los VFH_HV, pero que puede ser calculado con los campos pickup_datetime y dropoff_datetime. 

Para los taxis verdes (green) la información es prácticamente la misma que los amarillos, excepto que no hay campo airport_fee, ya que los verdes no van a aeropuertos. 

Los vehículos FOR HIRE que no son de alta demanda (FHV) no cuentan con información respecto a importes y total en dinero. Pero son tan poco respecto a los otros tipos de servicio, que se podrían omitir del estudio. 

Hay algunos valores en algunos campos que pudieran ser erroneos pues se presentan como outliers muy marcados. Para más información consultar los notebooks descritos anteriormente. 

### Medición del aire en la ciudad de Nueva York

Un primer acercamiento a la medición de los contaminantes se hizo através del estudio del NYC Open Data 'Air quality' que puede ser consultado en el link: 
https://data.cityofnewyork.us/Environment/Air-Quality/c3uy-2p5r

El estudio no cuenta con información desagregada por día ni hora, por lo que se decidió consultar otras fuentes de información. Se puede consultar el notebook dónde se analizó este dataset: 

• 'air.ipynb' 

y el documento:

• 'ANÁLISIS DESCRIPTIVO DEL REPORTE DE CALIDAD DEL AIRE.docx' 

Através del New York State Department of Environmental Conservation • Air Monitoring Website se encontró información sobre mediciones de contaminantes reportados de manera desagregada por día y por hora. El link para consultar y descargar reportes es el siguiente: 

http://www.nyaqinow.net/

Para consultar información complementaría sobre la ubicación de las estaciones de medición y su alcance se utilizó información de EPA AirData Quality Monitors. 

EPA "Environmental Protection Agency" (Agencia de Protección Ambiental) en inglés. Es una agencia federal de los Estados Unidos encargada de proteger la salud humana y el medio ambiente mediante la regulación de la contaminación del aire, agua y suelo, entre otras funciones.

La información se obtuvo del siguiente link: 

https://epa.maps.arcgis.com/apps/webappviewer/index.html?id=5f239fd3e72f424f98ef3d5def547eb5&extent=-146.2334,13.1913,-46.3896,56.5319

El proceso se explica en el notebook: 

• 'stations_info.ipynb' 

En dicho notebook se encuentra el proceso que se siguió para obtener las coordenadas de localización de las estaciones de medición de calidad del aire en la ciudad de Nueva York, así como el radio de alcance que tiene cada medición según el parámetro de contaminación que se esté utilizando. 

El mismo notebook se encuentra en formato PDF bajo el nombre 'Generación de coordenadas y radios de alcance para contaminantes por estación.pdf'

Para conocer la manera en que se seleccionaron las zonas TLC para las que se buscará relación con el contaminante PM 2.5 contra las mediciones de cada estación de medición, se puede consultar el notebook:

• 'zonas_medicion.ipynb'


