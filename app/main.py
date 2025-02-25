import sqlite3
import pandas as pd
import numpy as np

from fastapi import FastAPI
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

MOVIES_DATASET_PATH = '../assets/movies.csv'
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
    
    return f'{sum(cantidad)} cantidad de películas fueron estrenadas en el mes de {name_month}'


@app.get('/cantidad_filmaciones_dia/{name_day}')
def cantidad_filmaciones_dia(name_day: str):
    """
    Se ingresa el nombre del dia y regresa la cantidad de peliculas estrenadas en dicho día.
    """

    cantidad = 0
    count = 0
    weekdays = {
        'lunes': '1', 'martes': '2', 'miercoles': '3', 'jueves': '4', 'viernes': '5', 'sabado': '6', 'domingo': '0'
    }

    num_weekday = weekdays.get(name_day)

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cantidad = conn.execute("SELECT count(*) FROM movies WHERE strftime('%w', release_date) = ?", (num_weekday,)).fetchone()

    return f'{sum(cantidad)} cantidad de películas fueron estrenadas en los días {name_day}'


@app.get('/score_titulo/{title}')
def score_titulo(title: str):
    """
    Ingresa el nombre de una pelicula y regresa el año en que fue estrenada junto con el score obtenido.
    """

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        movie = conn.execute("SELECT release_year, vote_average FROM movies WHERE title = ?", (title,)).fetchone()

    return f"La película {title} fue estrenada en el año {movie[0]} con un score/popularidad de {movie[1]}"


@app.get('/votos_titulo/{title}')
def votos_titulo(title: str):
    """
    Ingresa el nombre de la pelicula y en caso que tenga mas de 2000 valoraciones regresa la cantidad de valoraciones con su score total,
    en caso de tener menos de 2000 valoraciones solo se envia mensaje que dicha pelicula no tiene las suficientes valoraciones.
    """

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        movie = conn.execute("SELECT release_year, vote_count, vote_average FROM movies WHERE title = ?", (title,)).fetchone()

    if movie[1] > 2000:
        return f"La película {title} fue estrenada en el año {movie[0]}. La misma cuenta con un total de {movie[1]} valoraciones, con un promedio de {movie[2]}"
    else:
        return f"La película {title} no cumple con las 2000 minimas valoraciones para arrojar el resultado"
    

@app.get('/get_actor/{name_actor}')
def get_actor(name_actor: str):
    """
    Ingresa el nombre de un actor y regresa la cantidad de peliculas en las que ha participado junto con el revenue total que ha obtenido en dichas peliculas.
    """

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        actor = conn.execute("SELECT movies, revenue FROM actors WHERE [cast] = ?", (name_actor,)).fetchone()

    return f"El actor {name_actor} ha participado de {actor[0]} cantidad de filmaciones, el mismo ha conseguido un revenue de {actor[1]} con un promedio de {actor[1]/actor[0]} por filmación"


@app.get('/get_director/{name_director}')
def get_director(name_director: str):
    """
    Ingresa el nombre de un director y regresa un diccionario estructurado de la siguiente manera:
    {
  "Name": "Michael Bay",
  "Success": [
    [6.21428571428571]
  ],
  "Movies": [
    [
      "Bad Boys",
      "1995-04-07",
      7.44247494736842, 19000000, 141407024, 6.5],
    [
      "Bad Boys II",
      "2003-07-18",
      2.10261196923077, 130000000, 273339556, 6.3],
    [
      "Transformers",
      "2007-06-27",
      4.73139853333333, 150000000, 709709780, 6.6],
    [
      "Transformers: Revenge of the Fallen",
      "2009-06-19",
      5.57531485333333, 150000000, 836297228, 6],
    [
      "Transformers: Dark of the Moon",
      "2011-06-28",
      5.76280510769231, 195000000, 1123746996, 6.1],
    [
      "Transformers: Age of Extinction",
      "2014-06-25",
      5.19716712857143, 210000000, 1091405097, 5.8],
    [
      "Transformers: The Last Knight",
      "2017-06-21",
      2.32670055, 260000000, 604942143, 6.2]
  ]
}
    """

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        director = conn.execute("SELECT m.title, m.release_date, m.return, m.budget, m.revenue, m.vote_average FROM directors d JOIN movies m ON d.id = m.id WHERE d.name = ?", (name_director,)).fetchall()
        success = conn.execute("SELECT avg(vote_average) FROM directors d JOIN movies m ON d.id = m.id WHERE d.name = ?", (name_director,)).fetchall()

    director_dic = {
        'Name': name_director,
        'Success': success,
        'Movies': director
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