from fastapi import FastAPI
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
environmen_database = MongoClient(f"mongodb://{usrname}:{passwd}@linebot-iot-mongodb-1:27017/")

@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("cn/bigproj/setting/device/c466") #subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)

@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print("Received message: ",topic, payload.decode())
    collection = environmen_database.env_device_data
    data = json.loads(payload.decode())
    post = { "device_id": topic[4],"timestamp": datetime.now(), "humidity": data["humid"], "temperature": data["temp"], "pressure": data["pressure"]}
    collection.insert_one(post)
    return 0

@app.get("/")
async def func():
    collection = environmen_database.env_device_data
    post = collection.find_one(sort= [( '_id', pymongo.DESCENDING)])
    post.pop("_id")
    return post