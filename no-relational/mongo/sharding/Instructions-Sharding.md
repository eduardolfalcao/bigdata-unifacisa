# Deploy and Use Mongo through Atlas

## Mongo Deployment (with sharding)

Ref: https://docs.mongodb.com/manual/tutorial/deploy-shard-cluster/

Firtst, let's create a network so that containers can communicate:
```bash
sudo docker network create mongo-shard
```

Now, we create ConfigServers Containers, one per Shard.
To do so, we use mongo image, with --configsvr, which means we're running the ConfigServer.
```bash
sudo docker run --name mongo-config01 --net mongo-shard -d mongo mongod --configsvr --replSet configserver --port 27017 --dbpath data/db
sudo docker run --name mongo-config02 --net mongo-shard -d mongo mongod --configsvr --replSet configserver --port 27017 --dbpath data/db
```

After starting ConfigServer, we need to set them up.
To do this, access shell of mongo in one of ConfigServer containers:
```bash
sudo docker exec -it mongo-config01 mongo
```

Then, initiate ConfigServers with the following command:
```bash
rs.initiate(
   {
      _id: "configserver",
      configsvr: true,
      version: 1,
      members: [
         { _id: 0, host : "mongo-config01:27017" },
         { _id: 1, host : "mongo-config02:27017" }
      ]
   }
)
```

Now, we proceed to create the shards.
We are going to create two shards, each with a replica, in total, six nodes.
We use mongo image with --shardsvr parameter, specifying this is a shard server.
```bash
# shard1, replicas A and B
sudo docker run --name mongo-shard1a --net mongo-shard -d mongo mongod --port 27018 --shardsvr --replSet shard01 --dbpath /data/db
sudo docker run --name mongo-shard1b --net mongo-shard -d mongo mongod --port 27018 --shardsvr --replSet shard01 --dbpath /data/db

# shard2, replicas A and B
sudo docker run --name mongo-shard2a --net mongo-shard -d mongo mongod --port 27019 --shardsvr --replSet shard02 --dbpath /data/db
sudo docker run --name mongo-shard2b --net mongo-shard -d mongo mongod --port 27019 --shardsvr --replSet shard02 --dbpath /data/db
```

Once deployed and running (online), we need to configure and initiate the shards.
To do that, we're going to access the shell of each of the shards (1 and 2), applying their respective setup.

```bash
sudo docker exec -it mongo-shard1a mongo --port 27018
# after accessing shell, run the following
rs.initiate(
   {
      _id: "shard01",
      version: 1,
      members: [
         { _id: 0, host : "mongo-shard1a:27018" },
         { _id: 1, host : "mongo-shard1b:27018" },
      ]
   }
)

sudo docker exec -it mongo-shard2a mongo --port 27019
# after accessing shell, run the following
rs.initiate(
   {
      _id: "shard02",
      version: 1,
      members: [
         { _id: 0, host : "mongo-shard2a:27019" },
         { _id: 1, host : "mongo-shard2b:27019" },
      ]
   }
)
```

Now, we need to deploy the Router, so that shards become accessible.
To initiate the Router we use mongo image, using the 'mongos' parameter.

```bash
sudo docker run -p 27017:27017 --name mongo-router --net mongo-shard -d mongo mongos --port 27017 --configdb configserver/mongo-config01:27017,mongo-config02:27017 --bind_ip_all
```

At this point, all services should be online. Check them through a 'docker ps' command.

Finally, we need to set up the Router to that it get to know the shards:
```bash
sudo docker exec -it mongo-router mongo

use _id
db.createUser(
    {
      user: "eduardolfalcao",
      pwd: "edu123",
      roles: [
         { role: "dbOwner", db: "_id" }
      ]
    }
,
    {
        w: "majority",
        wtimeout: 5000
    }
);

sh.addShard("shard01/mongo-shard1a:27018")
sh.addShard("shard01/mongo-shard1b:27018") 
sh.addShard("shard02/mongo-shard2a:27019")
sh.addShard("shard02/mongo-shard2b:27019")

sh.enableSharding("_id")
db.createCollection("_id.peopleCountCollection")
sh.shardCollection("_id.peopleCountCollection", {"collector_id" : "hashed"}) 

// verify that everything is ok with cluster
sh.status()
```

## Deploy Python Flask API to interact with Mongo

Config environment variables, build image of container with flask api, and run container with image freshly created:

```bash
export MONGO_IP=172.17.0.1
export DB_NAME=_id
export DB_USER=eduardolfalcao
export DB_PASSWORD=edu123

cd no-relational/mongo/sharding/api
sudo docker build -t api-mongo . && sudo docker run -e FLASK_APP=api-mongo.py -e DB_HOST=$MONGO_IP -e DB_NAME=$DB_NAME -e DB_USER=$DB_USER -e DB_PASSWORD=$DB_PASSWORD api-mongo:latest
```

## Using Mongo DB through the API

Discover IP of python flask API acting as façade for Mongo:
```bash
export FLASK_IP=$(sudo docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(sudo docker ps | grep api-mongo | cut -f 1 -d ' '))
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

