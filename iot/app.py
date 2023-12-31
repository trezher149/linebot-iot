from fastapi import FastAPI
from pydantic import BaseModel
from fastapi_mqtt import FastMQTT, MQTTConfig
from pymongo import MongoClient
import pymongo
import json
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

mqtt_config = MQTTConfig()
mqtt_config.host = "broker.hivemq.com"
mqtt = FastMQTT(config=mqtt_config)
mqtt.init_app(app)

usrname = os.environ.get("MONGO_INITDB_ROOT_USERNAME")
passwd = os.environ.get("MONGO_INITDB_ROOT_PASSWORD")
environmen_database = MongoClient(f"mongodb://{usrname}:{passwd}@mongodb:27017/")

class Device_id_Search(BaseModel):
    device_id: str

@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("cn/bigproj/device/c466") #subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)

@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print("Received message: ",topic, payload.decode())
    db = environmen_database.test_database
    collection = db.env_device_data
    data = json.loads(payload.decode())
    post = { "device_id": topic.split("/")[-1],"timestamp": datetime.now(), "humidity": data["humid"], "temperature": (data["temp"] / 100), "pressure": data["pressure"]}
    collection.insert_one(post)
    return 0

@app.get("/")
async def func():
    db = environmen_database.test_database
    collection = db.env_device_data
    post = collection.find_one(sort= [( '_id', pymongo.DESCENDING)])
    post.pop("_id")
    return post

# Below this line is apis for LINE Bot to use
# ======================================================================
@app.post("/api/linebot/environment_data")
async def line_environment_data(device_id: Device_id_Search):
    db = environmen_database.test_database
    collection = db.env_device_data
    data: dict = collection.find_one({'device_id': device_id.device_id}
        ,sort=[('temperature', pymongo.DESCENDING)])
    data.pop('_id')
    return data

@app.post("/api/front/environ_data")
async def front_environ_data(device_id: Device_id_Search):
    db = environmen_database.test_database
    collection = db.env_device_data
    cursor = collection.find({'device_id': device_id.device_id},sort= [( '_id', pymongo.DESCENDING)], limit=15)
    result_list = []
    for document in cursor:
        document["_id"] = str(document["_id"])
        result_list.append(document)
    return {
        "environ_data": result_list
    }