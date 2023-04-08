# taxis_NYC
NYC Taxis Data Science Project 

## Información sobre los movimientos de los taxis en la ciudad de Nueva York

La página de la NYC Taxi & Limousine Commission contiene información sobre los movimientos de los taxis amarillos, verdes, For hire vehicles (FHV), y for hire vehicles with high volume (dentro de esta categoría entra Uber y Lyft). 

La información está agrupada por mes y por servicio(yellow, green, FHV, FHV-HV) y puede ser consultada en este enlace: 
https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

Un análisis descriptivo de la información de los FHV-HV para el mes de enero de 2023 se encuentra en el notebook 'VFH_HV_analisis_descriptivo.ipynb' y en formato PDF en 'FHV_HV_analisis_descriptivo.pdf'


## Medición del aire en la ciudad de Nueva York

Un primer acercamiento a la medición de los contaminantes se hizo através del estudio del NYC Open Data 'Air quality' que puede ser consultado en el link: 
https://data.cityofnewyork.us/Environment/Air-Quality/c3uy-2p5r

El estudio no cuenta con información desagregada por día ni hora, por lo que se decidió consultar otras fuentes de información. Se puede consultar el notebook dónde se analizó este dataset: 'air.ipynb' y el documento 'ANÁLISIS DESCRIPTIVO DEL REPORTE DE CALIDAD DEL AIRE.docx' 

Através del New York State Department of Environmental Conservation • Air Monitoring Website se encontró información sobre mediciones de contaminantes reportados de manera desagregada por día y por hora. El para consultar y descargar reportes es el siguiente: 
http://www.nyaqinow.net/

Para consultar información complementaría sobre la ubicación de las estaciones de medición y su alcance se utilizó información de EPA AirData Quality Monitors. 

EPA "Environmental Protection Agency" (Agencia de Protección Ambiental) en inglés. Es una agencia federal de los Estados Unidos encargada de proteger la salud humana y el medio ambiente mediante la regulación de la contaminación del aire, agua y suelo, entre otras funciones.

La información se obtuvo del siguiente link: 
https://epa.maps.arcgis.com/apps/webappviewer/index.html?id=5f239fd3e72f424f98ef3d5def547eb5&extent=-146.2334,13.1913,-46.3896,56.5319

El proceso se explica en: 

En el notebook 'stations_info.ipynb' se encuentra el proceso que se siguió para obtener las coordenadas de localización de las estaciones de medición de calidad del aire en la ciudad de Nueva York, así como el radio de alcance que tiene cada medición según el parámetro de contaminación que se esté utilizando. 

El mismo notebook se encuentra en formato PDF bajo el nombre 'Generación de coordenadas y radios de alcance para contaminantes por estación.pdf'
