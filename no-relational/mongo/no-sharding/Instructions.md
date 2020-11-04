# Deploy and Use Mongo through Atlas

## Mongo Deployment (without sharding)

1. Access https://www.mongodb.com/cloud/atlas 
2. Build cluster: (feel free to change options)
    2.1. AWS; 
    2.2. North Virginia; 
    2.3. M0 SandBox; 
    2.4. MongoDB 4.2; 
    2.5. PeopleCounterAndRecognizer (name of project)
3. Create first database user ("Database Access"): 
    3.1. Choose login and password
    3.2. Choose read/write
4. Add IP on whitelist ("Network Access" tab):
    4.1. You can setup only your IP, or let it free to be accessible by anyone
5. Connect to your cluster (from Python, next section)

## Deploy Python Flask API to interact with Mongo

Be sure you have docker installed, running "docker --version".

Build image of container with flask api:
```bash
cd no-relational/mongo/no-sharding/api
sudo docker build -t api-mongo .
```

Get to know ip of MongoDB cluster, by navigating to "Clustes ==> Connect (button)"...
For instance, in the following line, this is the address of Mongo: peoplecounterandrecogni.08ezm.mongodb.net
```python
client = pymongo.MongoClient("mongodb+srv://eduardolfalcao:<password>@peoplecounterandrecogni.08ezm.mongodb.net/<dbname>?retryWrites=true&w=majority")
```

```bash
export MONGO_IP=peoplecounterandrecogni.08ezm.mongodb.net
export DB_NAME=iot_sensor
export DB_USER=eduardolfalcao
export DB_PASSWORD=edu123
```

Then, run flask api:
```bash
cd no-relational/mongo/no-sharding/api
sudo docker run -e FLASK_APP=api-mongo.py -e DB_HOST=$MONGO_IP -e DB_NAME=$DB_NAME -e DB_USER=$DB_USER -e DB_PASSWORD=$DB_PASSWORD api-mongo:latest
```

## Using Mongo DB through the API

Discover IP of python flask API acting as façade for Mongo:
```bash
export FLASK_IP=$(sudo docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(sudo docker ps | grep mongo | cut -f 1 -d ' '))
```

### Add people count
Add amount of people detected by given collector in given time.

* **URL**: `/add_people_count`
* **Method:** `POST`
* **Parameters**:
    1. `value` - people count (int)
    2. `collector_id` - collector iot device identification (string)
    3. `timestamp` - timestamp of detection (int)

* **Request example with CURL**:
```bash
curl http://$FLASK_IP:8080/add_people_count \
     --request POST --header "Content-Type: application/json" \
     --data '{
              "value": 23, 
              "collector_id": "iot_dev_id_1", 
              "timestamp": 342342
             }'
```

### Get people count
Get all people counted.

* **URL**: `/get_people_count`
* **Method:** `GET`
* **Parameters**: none

* **Request example with CURL**:
```bash
curl http://$FLASK_IP:8080/get_people_count --request GET 
```

### Add people recognized
Add people recognized by given sensor in given time.

* **URL**: `/add_people_recognized`
* **Method:** `POST`
* **Parameters**:
    1. `value` - list of people's name recognized (list of string)
    2. `collector_id` - collector iot device identification (string)
    3. `timestamp` - timestamp of detection (int)

* **Request example with CURL**:
```bash
curl http://$FLASK_IP:8080/add_people_recognized \
     --request POST --header "Content-Type: application/json" \
     --data '{
              "value": ["andrey", "eduardo", "fabio"], 
              "collector_id": "iot_dev_id_2", 
              "timestamp": 3423
             }'
```

### Get people recognized
Get all people recognized.

* **URL**: `/get_people_recognized`
* **Method:** `GET`
* **Parameters**: none

* **Request example with CURL**:
```bash
curl http://$FLASK_IP:8080/get_people_recognized --request GET 
```

