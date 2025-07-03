## Entrega

Este repositorio refleja el trabajo realizado a lo largo de las clases, incluyendo la participación
de todos los integrantes del grupo. El historial de commits muestra la evolución del proyecto desde
su estructura inicial hasta la versión final presentada.  

El presente archivo `README.md` contiene las explicaciones necesarias sobre el funcionamiento del sistema y cómo ejecutarlo.

## Sistema de Transporte Multimodal

Este proyecto modela un sistema de transporte entre distintas ciudades que permite planificar itinerarios
optimizando tiempo o costo. Utiliza programación orientada a objetos, lectura de archivos CSV y estructuras
de datos eficientes para representar nodos, conexiones y solicitudes.

## Objetivo

El objetivo del sistema es calcular recorridos óptimos entre ciudades, teniendo en cuenta diferentes tipos
de transporte (ferroviario, automotor, naval y aéreo), restricciones de velocidad o carga, y los costos asociados
a cada medio. El sistema también evita ciclos en los caminos y valida que los datos sean consistentes y correctos.

## Funcionalidades

- Carga nodos (ciudades) desde un archivo CSV.
- Carga conexiones entre nodos con atributos según el tipo de transporte.
- Carga solicitudes de envío e identifica los caminos posibles.
- Calcula itinerarios óptimos según tiempo o costo.
- Genera gráficos acumulativos de distancia, tiempo y costo.
- Ignora filas mal cargadas sin detener la ejecución.
- Valida errores comunes como nodos repetidos, distancias negativas o tipos de transporte inválidos.

## Archivos principales

- `main.py`: punto de entrada del programa, ejecuta el flujo completo.
- `nodo.py`: define los nodos (ciudades) y su registro global.
- `conexion.py`: define las conexiones y sus tipos (ferroviaria, automotor, naval, aérea).
- `vehiculos.py`: contiene los vehículos con sus velocidades y costos.
- `solicitudes.py`: lee y modela las solicitudes de envío.
- `tramo.py`: representa un tramo individual del recorrido.
- `itinerario.py`: representa un itinerario completo con todos sus tramos.
- `kpi.py`: se encarga de calcular el itinerario óptimo.
- `graficos.py`: genera gráficos para visualizar los KPIs.
- `capacidad.py`: se encarga de calcular la carga llevada por cada vehiculo.
- `costos.py`: se encarga de calcular los costos de cada recorrido.

## Cómo ejecutar

1. Asegurate de tener Python instalado.
2. Cloná este repositorio o descargá los archivos.
3. Colocá los archivos CSV dentro del mismo directorio (o en una carpeta `data/`).
4. Ejecutá el archivo `main.py` desde tu entorno de desarrollo o desde la consola de Python.

## Requisitos

- Python 3.10 o superior
- Librerías: `csv`, `math`, `matplotlib.pyplot`

No es necesario instalar librerías externas, todas son parte de la biblioteca estándar excepto `matplotlib`, que puede instalarse con:
  pip intstall matplotlib


## Desafíos y aclaraciones

Durante el desarrollo enfrentamos algunos desafíos importantes:

- Al principio no estábamos seguros de cómo modelar correctamente la clase `Conexion` ni dónde almacenar la información de los modos de transporte. Finalmente, optamos por centralizar todo en la clase `Conexion`, lo que facilitó la búsqueda de caminos posibles a través de un diccionario de conexiones.
- Tuvimos confusiones con la definición de “tramo” que proponía la cátedra. Al principio lo entendíamos como una conexión directa, pero luego comprendimos que debíamos considerar un tramo como cada uso del vehículo en una conexión individual, y calcular los costos en función de eso.
- Encontramos dificultades al calcular el costo para conexiones fluviales, especialmente para detectar correctamente si un tramo era marítimo o fluvial.
- A la hora de generar la lógica no tuvimos tantas dudas pero el mayor desafío fue encontrar una estructura de datos válida para almacenar cada una de ellas. En este caso optamos por un diccionario el cual nos iba a permitir organizar todos los trayectos de una solicitud por una key y luego llamarlos más tarde para mostrárselo al usuario.
- Al calcular los costos se nos presentó el desafío de que cada uno de los vehículos tienen costos distintos que dependen de distintas cosas y nos costó mucho unificar la forma de calcular todos.
-  Relacionado con el cálculo de costos porque lo debíamos usar para encontrar los costos. Nosotros consideramos esto un desafío importante porque las cargas no solo dependen de los vehículos sino que también de las conexiones y tenía que integrar ambas cosas para poder llegar al resultado deseado. Finalmente pudimos desarrollar una función que cumplía con todos los requisitos.

Aclaraciones:

- Si la carga máxima o la velocidad máxima en una conexión es 0, significa que no hay restricción para ese atributo: se toma el valor propio del vehículo.
- Las unidades utilizadas en el sistema son:
  - Tiempo: minutos (luego formateado a horas)
  - Distancia: kilómetros
  - Carga: kilogramos

## Créditos

Trabajo práctico realizado para la materia 71.45-Estructura de Datos (2025)

**Grupo 6**
- Juan Grispo 
- Nicolas Merle
- Tomas Di Gregorio Giralt
- Tomas Raele D'Amico
- Guido Levit
- Joaquin Martinez Alberte

## Cambios Realizados

Agregamos Clases:

  Consideramos que agregar nuevas clases era una modificación necesaria para respetar mejor los principios de la Programación Orientada a Objetos.  
  La incorporación de clases como `Tramo` fue clave para mejorar la abstracción de nuestro sistema, ya que nos permite representar adecuadamente las características compartidas de los tramos.

  Además, la clase `Planificador` mejoró el encapsulamiento y la modularidad del programa:
  - Encapsulamiento: unifica funciones y métodos clave para procesar solicitudes y generar KPI.
  - Modularidad: divide el código en métodos más simples y comprensibles, facilitando el mantenimiento y la evolución del sistema.

Reorganización de Funciones Clave:

  Reubicamos algunas funciones que antes estaban en módulos sueltos, ubicándolas ahora en las clases correspondientes:

  - Los cálculos de costos fueron incorporados en la clase `Vehiculo`.
  - Los KPI fueron integrados directamente en la clase `Planificador`.

  Esto mejora el encapsulamiento, manteniendo cada comportamiento dentro de su clase responsable.

Cambios Adicionales

  También realizamos algunos ajustes menores pero importantes:

  - Validación mejorada: ahora no se permite que haya dos solicitudes con el mismo ID.
  - Restricción de botones: deshabilitamos botones que requerían información previa o no eran necesarios desde el inicio.
  - Se muestran todas las rutas posibles para cada solicitud, incluyendo todos los tramos.
  - Eliminamos números mágicos: ahora cada tramo tiene un ID numérico asignado.
  - Agregamos el diagrama de clases que se muestra más arriba.
  - Incorporamos lo solicitado: un nuevo KPI y gráficos históricos que permiten un análisis visual del desempeño del sistema.

## Implementaciones Finales

KPI Tráfico:
  Nuevo KPI que calcula la ruta con menos tránsito.

Gráficos Históricos:
  Se generan dos nuevos gráficos en base a los datos de todas las solicitudes procesadas:
  - Un gráfico de barras que muestra la cantidad de veces que se utilizó cada conexión.
  - Un gráfico de barras que muestra la cantidad total de vehículos utilizados por tipo.



