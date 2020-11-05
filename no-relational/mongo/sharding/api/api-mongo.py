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
        ret = "Error inserting in people count: "+str(exc_N)

    return ret, error

@app.route('/get_people_count', methods=['GET'])
def get_people_count():
    print('Get people count called!')

    ret = dict()
    error = True
    try:      
        db = get_database()
        peopleCountCollection = db[DB_NAME]["peopleCountCollection"]
        for doc in peopleCountCollection.find():
            people_count_doc = {
                "_id": str(doc['_id']),
                "value": str(doc['value']),
                "collector_id": doc['collector_id'],
                "timestamp": str(doc['timestamp']),
            }
            ret[str(doc['_id'])] = people_count_doc 
    except Exception as exc_N:
        ret = "Error retrieving data from people count: "+exc_N
    
    return ret, error

@app.route('/add_people_recognized', methods=['POST'])
def add_people_recognized():
    print('Add people recognized called!')
    print('Request' + str(request.data))

    ret = "Inserted in people recognized Successfully!"
    error = True
    try:      
        db = get_database()
        peopleRecognizedCollection = db[DB_NAME]["peopleRecognizedCollection"]
        peopleRecognizedCollection.insert_one(request.get_json())
        error = False

    except Exception as exc_N:
        ret = "Error inserting in people recognized"

    return ret, error

@app.route('/get_people_recognized', methods=['GET'])
def get_people_recognized():
    print('Get people recognized!')

    ret = dict()
    error = True
    try:      
        db = get_database()
        peopleRecognizedCollection = db[DB_NAME]["peopleRecognizedCollection"]
        for doc in peopleRecognizedCollection.find():
            people_recog_doc = {
                "_id": str(doc['_id']),
                "value": str(doc['value']),
                "collector_id": doc['collector_id'],
                "timestamp": str(doc['timestamp']),
            }
            ret[str(doc['_id'])] = people_recog_doc 
    except Exception as exc_N:
        ret = "Error retrieving data from people recognized: "+exc_N
    
    return ret, error

def get_database():
    db = pymongo.MongoClient("mongodb://"+DB_USER+":"+DB_PASSWORD+"@"+DB_HOST+":27017/"+DB_NAME, serverSelectionTimeoutMS=5000)
    #db = pymongo.MongoClient("mongodb://0.0.0.0:27017")
    return db
