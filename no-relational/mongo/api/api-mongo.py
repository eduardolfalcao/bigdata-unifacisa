import pymongo
from flask import Flask, request, json
from flask_cors import CORS
from os import environ

DB_HOST = environ.get('DB_HOST')
DB_NAME = environ.get('DB_NAME')
DB_USER = environ.get('DB_USER')
DB_PASSWORD = environ.get('DB_PASSWORD')

if DB_PASSWORD is not None:
    print('###################################')
    print('These are the environment variables: DB_HOST='+DB_HOST+', DB_NAME='+DB_NAME+', DB_USER='+DB_USER+', DB_PASSWORD='+DB_PASSWORD)
    print('###################################')
else:
    print('###################################')
    print('No environment variable appeared!')
    print('###################################')

app = Flask(__name__)
cors = CORS(app)

@app.route('/add_people_count', methods=['POST'])
def add_people_count():

    print('Add people count called!')
    print('Request' + str(request.data))

    ret = "Inserted in people count Successfully!"
    error = True
    try:      
        db = get_database()
        peopleCountCollection = db[DB_NAME]["peopleCountCollection"]
        peopleCountCollection.insert_one(request.get_json())
        error = False

    except Exception as exc_N:
        ret = "Error inserting in people count"

    return ret, error

def get_database():
    db = pymongo.MongoClient("mongodb+srv://"+DB_USER+":"+DB_PASSWORD+"@"+DB_HOST+"/"+DB_NAME+"?retryWrites=true&w=majority", serverSelectionTimeoutMS=5000)
    return db

