from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse, FileResponse
import psycopg2
import secrets

app = FastAPI()

conn = psycopg2.connect(
    host='localhost',
    database='api_db',
    user='postgres',
    password='5918',
    port='5432'
)
cursor = conn.cursor()


@app.post('/reg')  # registration
def registration():
    pass


@app.post('/auth')
def authenticate(data=Body()):
    login = data['username']
    password = data['password']
    query = "select username, password, token from users where username='" + \
            str(login) + "' and password='" + str(password) + "'"
    cursor.execute(query)
    result = cursor.fetchall()
    if result:
        for line in result:
            if (str(line[0]) == str(login)) & (str(line[1]) == str(password)):
                return {'token': line[2], 'message': 'Access granted'}
    else:
        return {'token': None, 'message': 'Access denied'}


def tokenGenerate() -> str:
    return secrets.token_urlsafe(7)


@app.get('/')
def profilePage():
    return FileResponse('profile.html')


@app.post('/profile')
def profile(data=Body()):
    token = data['token']
    if token:
        query = "SELECT name, surname FROM users WHERE token='" + token + "';"
        cursor.execute(query)
        result = cursor.fetchall()
        if result:
            return {'name': result[0][0],
                    'surname': result[0][1]}
    else:
        return HTMLResponse('<h1 style="color:red">You are not authenticated</h1>')


print(tokenGenerate())
