import sqlite3
from sqlite3 import Error

def connect_to_db():
    try:
        connection = sqlite3.connect('flairs.db')
        connection.execute("""
                    CREATE TABLE IF NOT EXISTS flairs (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        flair_name TEXT NOT NULL,
                        flair_id TEXT NOT NULL
                    );
                    """)
        
        return connection
    except Error as e:
        print(e)
        raise

def delete_all_flairs(connection):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM flairs")
    
    connection.commit()

def retrieve_flairs(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM flairs")
    
    return cursor.fetchall()

def insert_flair(connection, flair):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM flairs WHERE flair_id = ?", (flair['id'],))
    result = cursor.fetchone()

    if not result:
        connection.execute("INSERT INTO flairs (flair_name, flair_id) VALUES (?, ?)", (flair['text'], flair['id']))
        connection.commit()

def close_connection(connection):
    connection.close()