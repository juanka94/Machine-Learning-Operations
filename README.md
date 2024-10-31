# Machine-Learning-Operations (MLOps)

Este repo corresponde al proyecto individual del Bootcamp de SoyHenry para integrar todas las habilidades obtenidas como un Data Scientist.

## Contexto

Una start-up que provee servicios de agregación de plataformas de streaming, requiere implementar una API que realice consultas sobre un par de Datasets.

## Estructura del proyecto

### Transformaciones

Dentro de la carpeta **ETL** se encuentra un notebook con todos los pasos que se realizaron para poder obtener los Datasets para alimentar la **API**.

### Analisis exploratorio de los datos

En la carpeta **EDA** se localiza el análisis exploratorio de los datos almacenados en una notebook, aquí se realizó un rápido y breve análisis de los Datasets.

### Assets

Aquí se guardan los **Datasets** generados en la etapa de **Transformación**.

### API

La **API** se encuentra almacenada en la carpeta **app**, en donde podemos encontrar el archivo *requirements.txt* que contiene los módulos necesarios para ejecutar la **API**, asi como el archivo **main.py** donde se encuentran las siguientes consultas:

- /cantidad_filmaciones_mes/{mes}: Se ingresa un mes y la API retorna la cantidad de peliculas que se estrenaron en dicho mes.
- /cantidad_filmaciones_dia/{dia}: Se ingresa un día de la semana y la API retorna la cantidad de películas que se estrenaron en dicho día de la semana.
- /score_titulo/{titulo}: Se ingresa el título de una película y retorna el año en que se estrenó, junto con la calificación que se tiene valorada.
- /votos_titulo/{titulo}:  Se ingresa el título de una película y en caso que la película tenga más de 2000 valoraciones retorna el año en que fue estrenada, cantidad de valoraciones y el promedio de valoraciones. En caso que la película tenga menos de 2000 valoraciones, se retorna un mensaje donde indica que dicha película no cumple con las mínimas valoraciones.
- /get_actor/{nombre}: Se ingresa el nombre de un actor y retorna la cantidad de películas en que ha participado, el revenue que han conseguido esas películas y un promedio de revenue por película.
- /get_director/{nombre}: Se ingresa el nombre de un director y retorna un diccionario con el nombre del director, un promedio de las valoraciones de sus películas y una lista con las películas en las que ha participado.
- /recomendacion/{titulo}: Se ingresa el título de una película y retorna las cinco películas mejor valoradas con respecto al algoritmo de distancia de Levenshtein para medir la similitud en el título de la película solicitado.
