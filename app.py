import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request

load_dotenv()

app = Flask(__name__)

# url = os.environ.get("DATABASE_URL")  # gets variables from environment
# connection = psycopg2.connect(url)
INSERT_USER = os.environ.get("INSERT_USER")
DELETE_USER = os.environ.get("DELETE_USER")
UPDATE_USER = os.environ.get("UPDATE_USER")
SELECT_USER = os.environ.get("SELECT_USER")
INSERT_TEACHER = os.environ.get("INSERT_TEACHER")
SELECT_TEACHER = os.environ.get("SELECT_TEACHER")
UPDATE_TEACHER = os.environ.get("UPDATE_TEACHER")
DELETE_TEACHER = os.environ.get("DELETE_TEACHER")


def connect_to_database(database):
    """
    connects to postgres server on the given database
    sets autocommit to true to avoid dealing with transaction code
    :param database:
    :return:
    """
    conn = psycopg2.connect(host="localhost", database=database, user='vitor', password='postgres')
    print(f' [x] connected to {database} database')
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    return conn, cursor

@app.post("/api/users/create")
def create_users():

    data = request.get_json()

    conn_main, cursor_main = connect_to_database('postgres')
    conn_1, cursor_1 = connect_to_database('replica1')
    conn_2, cursor_2 = connect_to_database('replica2')
    conn_3, cursor_3 = connect_to_database('replica3')

    id = data["id"]
    name = data["name"]
    cursor_main.execute(INSERT_USER, (id, name))
    cursor_1.execute(INSERT_USER, (id, name))
    cursor_2.execute(INSERT_USER, (id, name))
    cursor_3.execute(INSERT_USER, (id, name))

    conn_main.commit() 
    conn_1.commit() 
    conn_2.commit() 
    conn_3.commit() 

    cursor_main.close() 
    conn_main.close()
    cursor_1.close() 
    conn_1.close() 
    cursor_2.close() 
    conn_2.close() 
    cursor_3.close() 
    conn_3.close()  

    return {"message": "user created"}

@app.post("/api/users/delete")
def delete_from_users():

    data = request.get_json()

    conn_main, cursor_main = connect_to_database('postgres')
    conn_1, cursor_1 = connect_to_database('replica1')
    conn_2, cursor_2 = connect_to_database('replica2')
    conn_3, cursor_3 = connect_to_database('replica3')

    id = data["id"]
    cursor_main.execute(DELETE_USER, (id,))
    cursor_1.execute(DELETE_USER, (id,))
    cursor_2.execute(DELETE_USER, (id,))
    cursor_3.execute(DELETE_USER, (id,))

    conn_main.commit() 
    conn_1.commit() 
    conn_2.commit() 
    conn_3.commit() 

    cursor_main.close() 
    conn_main.close()
    cursor_1.close() 
    conn_1.close() 
    cursor_2.close() 
    conn_2.close() 
    cursor_3.close() 
    conn_3.close()  

    return {"message": f"user {id} deleted"}

@app.post("/api/users/read")
def read_from_users():

    data = request.get_json()
    user_name = ''

    conn_main, cursor_main = connect_to_database('postgres')
    # conn_1, cursor_1 = connect_to_database('replica1')
    # conn_2, cursor_2 = connect_to_database('replica2')
    # conn_3, cursor_3 = connect_to_database('replica3')

    id = data["id"]
    cursor_main.execute(SELECT_USER,(id,))
    # cursor_1.execute(SELECT_USER, (id,))
    # cursor_2.execute(SELECT_USER, (id,))
    # cursor_3.execute(SELECT_USER, (id,))
    users = cursor_main.fetchall()

    conn_main.commit() 
    # conn_1.commit() 
    # conn_2.commit() 
    # conn_3.commit() 

    cursor_main.close() 
    conn_main.close()
    # cursor_1.close() 
    # conn_1.close() 
    # cursor_2.close() 
    # conn_2.close() 
    # cursor_3.close() 
    # conn_3.close()  

    return {"message": f"{users} fetched"}

@app.post("/api/users/update")
def update_on_users():
     
    data = request.get_json()

    conn_main, cursor_main = connect_to_database('postgres')
    conn_1, cursor_1 = connect_to_database('replica1')
    conn_2, cursor_2 = connect_to_database('replica2')
    conn_3, cursor_3 = connect_to_database('replica3')

    id = data["id"]
    name = data["name"]
    cursor_main.execute(UPDATE_USER, (name, id))
    cursor_1.execute(UPDATE_USER,  (name, id))
    cursor_2.execute(UPDATE_USER,  (name, id))
    cursor_3.execute(UPDATE_USER,  (name, id))

    conn_main.commit() 
    conn_1.commit() 
    conn_2.commit() 
    conn_3.commit() 

    cursor_main.close() 
    conn_main.close()
    cursor_1.close() 
    conn_1.close() 
    cursor_2.close() 
    conn_2.close() 
    cursor_3.close() 
    conn_3.close()   

    return {"message": f"{id}: {name} updated"}


@app.post("/api/teachers/create")
def create_teachers():

    data = request.get_json()

    conn_main, cursor_main = connect_to_database('postgres')
    conn_1, cursor_1 = connect_to_database('replica1')
    conn_2, cursor_2 = connect_to_database('replica2')
    conn_3, cursor_3 = connect_to_database('replica3')

    id = data["id"]
    name = data["name"]
    cursor_main.execute(INSERT_TEACHER, (id, name))
    cursor_1.execute(INSERT_TEACHER, (id, name))
    cursor_2.execute(INSERT_TEACHER, (id, name))
    cursor_3.execute(INSERT_TEACHER, (id, name))

    conn_main.commit() 
    conn_1.commit() 
    conn_2.commit() 
    conn_3.commit() 

    cursor_main.close() 
    conn_main.close()
    cursor_1.close() 
    conn_1.close() 
    cursor_2.close() 
    conn_2.close() 
    cursor_3.close() 
    conn_3.close()  

    return {"message": "teacher created"}

@app.post("/api/teachers/delete")
def delete_from_teachers():

    data = request.get_json()

    conn_main, cursor_main = connect_to_database('postgres')
    conn_1, cursor_1 = connect_to_database('replica1')
    conn_2, cursor_2 = connect_to_database('replica2')
    conn_3, cursor_3 = connect_to_database('replica3')

    id = data["id"]
    cursor_main.execute(DELETE_TEACHER, (id,))
    cursor_1.execute(DELETE_TEACHER, (id,))
    cursor_2.execute(DELETE_TEACHER, (id,))
    cursor_3.execute(DELETE_TEACHER, (id,))

    conn_main.commit() 
    conn_1.commit() 
    conn_2.commit() 
    conn_3.commit() 

    cursor_main.close() 
    conn_main.close()
    cursor_1.close() 
    conn_1.close() 
    cursor_2.close() 
    conn_2.close() 
    cursor_3.close() 
    conn_3.close()  

    return {"message": f"teacher {id} deleted"}

@app.post("/api/teachers/read")
def read_from_teachers():

    data = request.get_json()
    user_name = ''

    conn_main, cursor_main = connect_to_database('postgres')
    # conn_1, cursor_1 = connect_to_database('replica1')
    # conn_2, cursor_2 = connect_to_database('replica2')
    # conn_3, cursor_3 = connect_to_database('replica3')

    id = data["id"]
    cursor_main.execute(SELECT_TEACHER,(id,))
    # cursor_1.execute(SELECT_TEACHER, (id,))
    # cursor_2.execute(SELECT_TEACHER, (id,))
    # cursor_3.execute(SELECT_TEACHER, (id,))
    users = cursor_main.fetchall()

    conn_main.commit() 
    # conn_1.commit() 
    # conn_2.commit() 
    # conn_3.commit() 

    cursor_main.close() 
    conn_main.close()
    # cursor_1.close() 
    # conn_1.close() 
    # cursor_2.close() 
    # conn_2.close() 
    # cursor_3.close() 
    # conn_3.close()  

    return {"message": f"{users} fetched"}

@app.post("/api/teachers/update")
def update_on_teachers():
     
    data = request.get_json()

    conn_main, cursor_main = connect_to_database('postgres')
    conn_1, cursor_1 = connect_to_database('replica1')
    conn_2, cursor_2 = connect_to_database('replica2')
    conn_3, cursor_3 = connect_to_database('replica3')

    id = data["id"]
    name = data["name"]
    cursor_main.execute(UPDATE_TEACHER, (name, id))
    cursor_1.execute(UPDATE_TEACHER,  (name, id))
    cursor_2.execute(UPDATE_TEACHER,  (name, id))
    cursor_3.execute(UPDATE_TEACHER,  (name, id))

    conn_main.commit() 
    conn_1.commit() 
    conn_2.commit() 
    conn_3.commit() 

    cursor_main.close() 
    conn_main.close()
    cursor_1.close() 
    conn_1.close() 
    cursor_2.close() 
    conn_2.close() 
    cursor_3.close() 
    conn_3.close()   

    return {"message": f"{id}: {name} updated"}
