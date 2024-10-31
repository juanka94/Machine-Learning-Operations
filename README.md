# Machine-Learning-Operations (MLOps)

Este repo corresponde al proyecto individual del Bootcamp de SoyHenry para integrar todas las habilidades obtenidas como un Data Scientist.

## Contexto

Una start-up que provee servicios de agregación de plataformas de streaming, requiere implementar una API que realice consultas sobre un par de Datasets.

## Estructura del proyecto

### Transformaciones

Dentro de la carpeta **ETL** se encuentra un notebook con todos los pasos que se realizaron para poder obtener los Datasets para alimentar la API.

### Analisis exploratorio de los datos

En la carpeta **EDA** se localiza el analisis exploratorio de los datos almacenado en una notebook, aqui se realizo un rapido y brebe analisis de los Datasets.

### Assets

Aqui se guardan los **Datasets** generados en la etapa de **Transformacion**

### API

La **API** se encuentra almacenada en la carpeta **app**, en donde podemos encontrar el archivo requirements.txt que contiene los modulos necesarios para ejecturar la **API**, asi como el archivo **main.py** donde se encuentran las siguientes consultas:

- /cantidad_filmaciones_mes/{mes}: Se ingresa un mes y la API retorna la cantidad de peliculas que se estrenaron en dicho mes.
- /cantidad_filmaciones_dia/{dia}: Se ingresa un dia de la semana y la API retorna la cantidad de peliculas que se estrenaron en dicho dia de la semana.
- /score_titulo/{titulo}: Se ingresa el titulo de una pelicula y retorna el año en que se estreno, junto con la calificacion que se tiene valorada.
- /votos_titulo/{titulo}: Se ingresa el titulo de una pelicula y en caso que la pelicula tenga mas de 2000 valoraciones retorna el año en que fue estrenada, cantidad de valoraciones y el promedio de valoraciones. En caso que la pelicula tenga menos de 2000 valoraciones, se retorna un mensaje donde indica que dicha pelicula no cumple con las minimas valoraciones.
- /get_actor/{nombre}: Se ingresa el nombre de un actor y retorna la cantidad de peliculas en que ha participado, el revenue que han consigido esas peliculas y un promedio de revenue por pelicula.
- /get_director/{nombre}: Se ingresa el nombre de un director y retorna un diccionario con el nombre del director, un promedio de las valoraciones de sus peliculas y una lista con las peliculas en las que ha participado.
- /recomendacion/{titulo}: Se ingresa el titulo de una pelicula y retorna las cinco peliculas mejor valoradas con respecto en el algoritmo de distancia de Levenshtein para medir la similitud en el titulo de la pelicula solicitado.
