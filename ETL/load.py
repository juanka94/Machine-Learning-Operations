import sys
import pandas
import sqlite3


try:
    
    # Connect to DB and create a cursor
    conn = sqlite3.connect('./DB/cinema.db')
    cursor = conn.cursor()
    print('DB Init')

    # Write a query and execute it with cursor
    query = 'select sqlite_version();'
    cursor.execute(query)
 
    # Fetch and output result
    result = cursor.fetchall()
    print('SQLite Version is {}'.format(result))

    #Create tables
    #Genres
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
        CREATE TABLE IF NOT EXISTS collections(
            id INTEGER PRIMARY KEY,
            name TEXT,
            poster_path TEXT,
            backdrop_path
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
            return REAL,
            collection_id INTEGER,
            FOREIGN KEY(collection_id) REFERENCES collections(id)
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
        """)

    # Write a query and execute it with cursor
    query = 'PRAGMA table_info(movies_companies)'
    cursor.execute(query)
 
    # Fetch and output result
    result = cursor.fetchall()
    print('Table Info: {}'.format(result))

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