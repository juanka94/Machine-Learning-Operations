import pandas as pd
import numpy as np

from fastapi import FastAPI
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

MOVIES_DATASET_PATH = '../assets/movies.csv'
ACTORS_DATASET_PATH = '../assets/actors.csv'
DIRECTORS_DATASET_PATH = '../assets/directors.csv'

app = FastAPI()

@app.get('/')
def root():
    return {"Hello": "World"}


@app.get('/cantidad_filmaciones_mes/{name_month}')
def cantidad_filmaciones_mes(name_month: str):

    cantidad = 0
    count = 0
    months = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6,
        'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
    }


    num_month = months.get(name_month)

    movies = pd.read_csv(MOVIES_DATASET_PATH, delimiter=',', encoding='utf-8')

    release_months = pd.to_datetime(movies['release_date']).dt.month

    cantidad = [count + 1 for month in release_months if month == num_month]

    return f'{sum(cantidad)} cantidad de películas fueron estrenadas en el mes de {name_month}'


@app.get('/cantidad_filmaciones_dia/{name_day}')
def cantidad_filmaciones_dia(name_day: str):

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
    movies = pd.read_csv(MOVIES_DATASET_PATH, delimiter=',', encoding='utf-8')

    movie_index = movies.index.get_indexer_for((movies[movies.title == title].index)).tolist()
    movie = movies.iloc[movie_index[0]]

    return f"La película {movie['title']} fue estrenada en el año {movie['release_year']} con un score/popularidad de {movie['vote_average']}"


@app.get('/votos_titulo/{title}')
def votos_titulo(title: str):
    movies = pd.read_csv(MOVIES_DATASET_PATH, delimiter=',', encoding='utf-8')

    movie_index = movies.index.get_indexer_for((movies[movies.title == title].index)).tolist()
    movie = movies.iloc[movie_index[0]]

    if movie['vote_count'] > 2000:
        return f"La película {movie['title']} fue estrenada en el año {movie['release_year']}. La misma cuenta con un total de {movie['vote_count']} valoraciones, con un promedio de {movie['vote_average']}"
    else:
        return f"La película {movie['title']} no cumple con las 2000 minimas valoraciones para arrojar el resultado"
    

@app.get('/get_actor/{name_actor}')
def get_actor(name_actor: str):
    actors = pd.read_csv(ACTORS_DATASET_PATH, delimiter=',', encoding='utf-8')

    actor_index = actors.index.get_indexer_for((actors[actors.cast == name_actor].index)).tolist()
    actor = actors.iloc[actor_index[0]]

    return f"El actor {actor['cast']} ha participado de {actor['movies']} cantidad de filmaciones, el mismo ha conseguido un revenue de {actor['revenue']} con un promedio de {actor['revenue']/actor['movies']} por filmación"


@app.get('/get_director/{name_director}')
def get_director(name_director: str):
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
    movies = pd.read_csv(MOVIES_DATASET_PATH, delimiter=',', encoding='utf-8')

    movies['similarity'] = movies['title'].apply(lambda x: fuzz.ratio(x, title))

    recommended_movies = movies.sort_values(['similarity', 'vote_average'], ascending=[False, False])

    return recommended_movies.head(5)[['title']]