import sqlite3
import itertools
import ast
import numpy as np
import pandas as pd

try:
    
    # Conectar DB y crear cursor
    conn = sqlite3.connect('./DB/cinema.db')
    cursor = conn.cursor()
    print('DB Init')

    #Obtener version de SQLite
    query = 'select sqlite_version();'
    cursor.execute(query)
 
    # Fetch and output result
    result = cursor.fetchall()
    print('SQLite Version is {}'.format(result))

    #Create tables
    print('Creando tablas...')
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS genres(
            id INTEGER PRIMARY KEY,
            name TEXT
                );
        CREATE TABLE IF NOT EXISTS languages(
            code TEXT PRIMARY KEY,
            name TEXT    
                );
        CREATE TABLE IF NOT EXISTS production_companies(
            id INTEGER PRIMARY KEY,
            name TEXT
                );
        CREATE TABLE IF NOT EXISTS production_countries(
            code INTEGER PRIMARY KEY,
            name TEXT
                );
        CREATE TABLE IF NOT EXISTS movies(
            id INTEGER PRIMARY KEY,
            title TEXT not NULL,
            release_date TEXT,
            release_year TEXT,
            overview TEXT,
            Tagline TEXT,
            runtime REAL,
            status TEXT,
            popularity REAL,
            vote_count INTEGER,
            vote_average REAL,
            budget REAL,
            revenue REAL,
            return REAL
                );
        CREATE TABLE IF NOT EXISTS actors(
            id INTEGER PRIMARY KEY,
            name TEXT,
            revenue REAL,
            movies INTEGER,
            return REAL            
                );
        CREATE TABLE IF NOT EXISTS directors(
            id INTEGER PRIMARY KEY,
            name TEXT
                );
        CREATE TABLE IF NOT EXISTS movies_genres(
            movie_id INTEGER not NULL REFERENCES movies(id) ON DELETE CASCADE ON UPDATE CASCADE,
            genre_id INTEGER not NULL REFERENCES genre(id) ON DELETE CASCADE ON UPDATE CASCADE,
            PRIMARY KEY (movie_id, genre_id)            
            );
        CREATE TABLE IF NOT EXISTS movies_languages(
            movie_id INTEGER not NULL REFERENCES movies(id) ON DELETE CASCADE ON UPDATE CASCADE,
            language_id INTEGER not NULL REFERENCES languages(code) ON DELETE CASCADE ON UPDATE CASCADE,
            PRIMARY KEY (movie_id, language_id)            
            );
        CREATE TABLE IF NOT EXISTS movies_countries(
            movie_id INTEGER not NULL REFERENCES movies(id) ON DELETE CASCADE ON UPDATE CASCADE,
            country_id INTEGER not NULL REFERENCES country(id) ON DELETE CASCADE ON UPDATE CASCADE,
            PRIMARY KEY (movie_id, country_id)            
            );
        CREATE TABLE IF NOT EXISTS movies_companies(
            movie_id INTEGER not NULL REFERENCES movies(id) ON DELETE CASCADE ON UPDATE CASCADE,
            company_id INTEGER not NULL REFERENCES company(id) ON DELETE CASCADE ON UPDATE CASCADE,
            PRIMARY KEY (movie_id, company_id)            
            );
        CREATE TABLE IF NOT EXISTS movies_directors(
            movie_id INTEGER not NULL REFERENCES movies(id) ON DELETE CASCADE ON UPDATE CASCADE,
            director_id INTEGER not NULL REFERENCES director(id) ON DELETE CASCADE ON UPDATE CASCADE,
            PRIMARY KEY (movie_id, director_id)
            );
        """)
    print('Tablas creadas...')

    # Abrir CSV Peliculas
    movies = pd.read_csv('./assets/movies.csv', delimiter=',', encoding='utf-8')
    # Total filas en el Dataframe
    row_count = len(movies)

    # Obtenemos solo las filas que aun no existen en nuestra DB
    query = "SELECT id FROM movies WHERE id IN ({seq})".format(seq=','.join(['?']*len(movies)))
    ids_duplicated = pd.read_sql_query(query, conn, params=tuple(movies['id']))
    ids_on_db = movies['id'].isin(ids_duplicated['id'])
    movies_to_load = movies[~ids_on_db]
    movies_to_load[['genres','production_companies','production_countries','spoken_languages']] = movies_to_load[['genres','production_companies','production_countries','spoken_languages']].map(ast.literal_eval)

    # Cargamos genres
    genres = movies_to_load['genres']
    flattened_list = list(itertools.chain(*genres))
    genres = pd.DataFrame(flattened_list).drop_duplicates(subset='name').reset_index(drop=True)
    genres.drop('id', axis=1, inplace=True)
    genres.to_sql(name='genres', con=conn, if_exists='replace')

    #Cargamos languages
    languages = movies_to_load['spoken_languages']
    flattened_list = list(itertools.chain(*languages))
    languages = pd.DataFrame(flattened_list).drop_duplicates(subset='name').reset_index(drop=True)
    languages.rename(columns={'iso_639_1': 'code'}, inplace=True)
    languages.to_sql(name='languages', con=conn, if_exists='replace')

    #Cargamos companies
    companies = movies_to_load['production_companies']
    flattened_list = list(itertools.chain(*companies))
    companies = pd.DataFrame(flattened_list).drop_duplicates(subset='name').reset_index(drop=True)
    companies.drop('id', axis=1, inplace=True)
    companies.to_sql(name='companies', con=conn, if_exists='replace')

    #Cargamos countries
    countries = movies_to_load['production_countries']
    flattened_list = list(itertools.chain(*countries))
    countries = pd.DataFrame(flattened_list).drop_duplicates(subset='name').reset_index(drop=True)
    countries.rename(columns={'iso_3166_1': 'code'}, inplace=True)
    countries.to_sql(name='countries', con=conn, if_exists='replace')

    #Cargamos movies
    movies_to_load.drop(['belongs_to_collection', 'original_language', 'genres','production_companies','production_countries','spoken_languages'], axis=1, inplace=True)
    movies_to_load.to_sql(name='movies', con=conn, if_exists='replace')
    
    result = cursor.execute("""SELECT * From movies""").fetchall()

    print(result)

    conn.commit()
 
    # Close the cursor
    cursor.close()

except sqlite3.Error as error:
    print('Error occurred - ', error)
 
# Close DB Connection irrespective of success
# or failure
finally:

    if conn:
        conn.close()
        print('SQLite Connection closed')