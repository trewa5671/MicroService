from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from mysql.connector import connect, Error
import os

app = FastAPI()

def start_con():
    try:
        connection = connect(
            host=os.getenv('MYSQL_HOST', 'mysql_db'),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', 'qwerty'),
        )
        print(connection)
        create_db_query = "CREATE DATABASE IF NOT EXISTS recipes"
        use_db_query = "USE recipes"
        create_table_query = "CREATE TABLE IF NOT EXISTS recipes (id int)"
        with connection.cursor() as cursor:
            cursor.execute(create_db_query)
            cursor.execute(use_db_query)
            cursor.execute(create_table_query)
        connection.commit()
    except Error as e:
        print(e)
        return
    return connection

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/')
async def root(id: int):
    connection = start_con()
    if not connection:
        return
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"INSERT INTO recipes VALUES ({id})")
        connection.commit()
    except Error as e:
        print(e)
    return 1

@app.get('/')
async def get_data():
    connection = start_con()
    if not connection:
        return
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT id FROM recipes.recipes")
            return [j for i in cursor.fetchall() for j in i]
    except Error as e:
        print(e)
    return list()

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=3001)