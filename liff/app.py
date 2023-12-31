from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import pymongo
from pymongo import MongoClient
import os

mongo_host = os.environ["MONGO_HOST"]
usrname = os.environ["MONGO_INITDB_ROOT_USERNAME"]
passwd = os.environ["MONGO_INITDB_ROOT_PASSWORD"]
mongo_client = MongoClient(f"mongodb://{usrname}:{passwd}@{mongo_host}")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/test")
async def test_endpoint():
    return 'OK'

@app.get("/", response_class=HTMLResponse)
async def liff_html(request: Request):
    data = get_iot_data()
    return templates.TemplateResponse("index.html", context={"request": request, "data": data})

def get_iot_data():
    db = mongo_client.test_database
    collection = db.test_collection
    data = collection.find({}, sort=[('_id', pymongo.DESCENDING)], limit=15)
    return list(data)
