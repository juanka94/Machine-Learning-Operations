import sqlite3
import pandas as pd
import numpy as np

from fastapi import FastAPI
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

MOVIES_DATASET_PATH = '../assets/movies.csv'
ACTORS_DATASET_PATH = '../assets/actors.csv'
DIRECTORS_DATASET_PATH = '../assets/directors.csv'
DB_PATH = '../DB/cinema.db'

app = FastAPI()

@app.get('/')
def root():
    return f"Proyecto Individual MLOps - Juan Carlos Ruiz Navarro"


@app.get('/cantidad_filmaciones_mes/{name_month}')
def cantidad_filmaciones_mes(name_month: str):
    """
    Se ingresa el nombre del mes y regresa la cantidad de peliculas que se estrenaron en dicho mes.
    """
    cantidad = 0
    months = {
        'enero': '01', 'febrero': '02', 'marzo': '03', 'abril': '04', 'mayo': '05', 'junio': '06',
        'julio': '07', 'agosto': '08', 'septiembre': '09', 'octubre': '10', 'noviembre': '11', 'diciembre': '12'
    }

    num_month = months.get(name_month)

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cantidad = conn.execute("SELECT count(*) FROM movies WHERE strftime('%m', release_date) = ?", (num_month,)).fetchone()
        print(cantidad)
    
    return f'{sum(cantidad)} cantidad de películas fueron estrenadas en el mes de {name_month}'


@app.get('/cantidad_filmaciones_dia/{name_day}')
def cantidad_filmaciones_dia(name_day: str):
    """
    Se ingresa el nombre del dia y regresa la cantidad de peliculas estrenadas en dicho día.
    """

    cantidad = 0
    count = 0
    weekdays = {
        'lunes': 0, 'martes': 1, 'miercoles': 2, 'jueves': 3, 'viernes': 4, 'sabado': 5, 'domingo': 6
    }

    num_weekday = weekdays.get(name_day)

    movies = pd.read_csv(MOVIES_DATASET_PATH, delimiter=',', encoding='utf-8')

    release_weekdays = pd.to_datetime(movies['release_date']).dt.weekday

    cantidad = [count + 1 for weekday in release_weekdays if weekday == num_weekday]

    return f'{sum(cantidad)} cantidad de películas fueron estrenadas en los días {name_day}'


@app.get('/score_titulo/{title}')
def score_titulo(title: str):
    """
    Ingresa el nombre de una pelicula y regresa el año en que fue estrenada junto con el score obtenido.
    """

    movies = pd.read_csv(MOVIES_DATASET_PATH, delimiter=',', encoding='utf-8')

    movie_index = movies.index.get_indexer_for((movies[movies.title == title].index)).tolist()
    movie = movies.iloc[movie_index[0]]

    return f"La película {movie['title']} fue estrenada en el año {movie['release_year']} con un score/popularidad de {movie['vote_average']}"


@app.get('/votos_titulo/{title}')
def votos_titulo(title: str):
    """
    Ingresa el nombre de la pelicula y en caso que tenga mas de 2000 valoraciones regresa la cantidad de valoraciones con su score total,
    en caso de tener menos de 2000 valoraciones solo se envia mensaje que dicha pelicula no tiene las suficientes valoraciones.
    """

    movies = pd.read_csv(MOVIES_DATASET_PATH, delimiter=',', encoding='utf-8')

    movie_index = movies.index.get_indexer_for((movies[movies.title == title].index)).tolist()
    movie = movies.iloc[movie_index[0]]

    if movie['vote_count'] > 2000:
        return f"La película {movie['title']} fue estrenada en el año {movie['release_year']}. La misma cuenta con un total de {movie['vote_count']} valoraciones, con un promedio de {movie['vote_average']}"
    else:
        return f"La película {movie['title']} no cumple con las 2000 minimas valoraciones para arrojar el resultado"
    

@app.get('/get_actor/{name_actor}')
def get_actor(name_actor: str):
    """
    Ingresa el nombre de un actor y regresa la cantidad de peliculas en las que ha participado junto con el revenue total que ha obtenido en dichas peliculas.
    """

    actors = pd.read_csv(ACTORS_DATASET_PATH, delimiter=',', encoding='utf-8')

    actor_index = actors.index.get_indexer_for((actors[actors.cast == name_actor].index)).tolist()
    actor = actors.iloc[actor_index[0]]

    return f"El actor {actor['cast']} ha participado de {actor['movies']} cantidad de filmaciones, el mismo ha conseguido un revenue de {actor['revenue']} con un promedio de {actor['revenue']/actor['movies']} por filmación"


@app.get('/get_director/{name_director}')
def get_director(name_director: str):
    """
    Ingresa el nombre de un director y regresa un diccionario estructurado de la siguiente manera:
    {
        "Name": "Tim Burton", #Nombre del director
        "Success": 6.65, #Promedio de valoraciones de todas sus peliculas
        "Movies": [ #Lista de diccionarios con las peliculas del director
            {
                "title": {
                    "74": "Batman"
                },
                "release_date": {
                    "74": "1989-06-23"
                },
                "return": {
                    "74": 11.7528264
                },
                "budget": {
                    "74": 35000000
                },
                "revenue": {
                    "74": 411348924
                },
                "vote_average": {
                    "74": 7
                }
            },
            .
            .
            .
        ]
    }
    """

    directors = pd.read_csv(DIRECTORS_DATASET_PATH,delimiter=',', encoding='utf-8')
    movies = pd.read_csv(MOVIES_DATASET_PATH, delimiter=',', encoding='utf-8')

    director_movies = []
    director_success = []

    movies_id = directors[directors.name == name_director]['id']
    for movie in movies_id:
        #movie_index = movies.index.get_indexer_for((movies[movies['id'] == movie].index)).tolist()
        director_movies.append(movies.loc[movies['id'] == movie].filter(['title', 'release_date', 'return', 'budget', 'revenue', 'vote_average']))
    
    for movie in director_movies:
       director_success.append(movie['vote_average'].tolist()[0])

    director_success = sum(director_success)/len(director_success)

    director_dic = {
        'Name': name_director,
        'Success': director_success,
        'Movies': director_movies
    }

    print(director_dic)

    return director_dic


@app.get('/recomendacion/{title}')
def recomendacion(title: str):
    """
    Ingresa el titulo de una pelicula y regresa las 5 peliculas mas similares en el titulo y que sean las mejor valoradas.
    """
    movies = pd.read_csv(MOVIES_DATASET_PATH, delimiter=',', encoding='utf-8')

    movies['similarity'] = movies['title'].apply(lambda x: fuzz.ratio(x, title))

    recommended_movies = movies.sort_values(['similarity', 'vote_average'], ascending=[False, False])

    return recommended_movies.head(5)[['title']]