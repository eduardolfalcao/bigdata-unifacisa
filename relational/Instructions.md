# Deploy and Use MariaDB

## Maria Deployment

Be sure you have docker install, running "docker --version".
If you don't have it, then do the following:
```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository    "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io
sudo usermod -aG docker $USER
docker --version
```

Now, build image, from within "relational/maria" directory:
```bash
cd relational/maria
sudo docker build -t maria .
```

Then, run maria:
```bash
export DB_PASSWORD=edu123
sudo docker run -e MYSQL_ROOT_PASSWORD=$DB_PASSWORD maria
```

## Deploy Python Flask API to interact with Maria

Build image of container with flask api:
```bash
cd relational/api
sudo docker build -t api-maria .
```

Get to know ip of DB:
```bash
export MARIA_IP=$(sudo docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(sudo docker ps | grep maria | cut -f 1 -d ' '))
```

Then, run flask api:
```bash
cd relational/api
sudo docker run -e FLASK_APP=api-maria.py -e DB_HOST=$MARIA_IP -e DB_NAME=iot_sensor -e DB_USER=root -e DB_PASSWORD=edu123 api-maria:latest
```

## Using Maria DB through the API

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
curl http://172.17.0.3:8080/add_people_count \
     --request POST --header "Content-Type: application/json" \
     --data '{
              "value": 23, 
              "collector_id": "iot_dev_id_1", 
              "timestamp": 342342
             }'
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
curl http://172.17.0.3:8080/add_people_recognized \
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
curl http://172.17.0.3:8080/get_people_recognized --request GET 
```

