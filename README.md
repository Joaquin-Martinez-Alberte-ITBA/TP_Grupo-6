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

- Al principio no estábamos seguros de cómo modelar correctamente la clase `Conexion` ni dónde almacenar la información de
  los modos de transporte. Finalmente, optamos por centralizar todo en la clase `Conexion`, lo que facilitó la búsqueda de caminos
  posibles a través de un diccionario de conexiones.
- Tuvimos confusiones con la definición de “tramo” que proponía la cátedra. Al principio lo entendíamos como una conexión
  directa, pero luego comprendimos que debíamos considerar un tramo como cada uso del vehículo en una conexión individual,
  y calcular los costos en función de eso.
- Encontramos dificultades al calcular el costo para conexiones fluviales, especialmente para detectar correctamente si un tramo era marítimo o fluvial.

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

