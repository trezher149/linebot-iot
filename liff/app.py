from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from dotenv import load_dotenv
import asyncio
import os
from pymongo import MongoClient
import pymongo
import json

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

usrname = os.environ.get("MONGO_INITDB_ROOT_USERNAME")
passwd = os.environ.get("MONGO_INITDB_ROOT_PASSWORD")
mongo_client = MongoClient(f"mongodb://{usrname}:{passwd}@linebot-iot-mongodb-1:27017/")
db = mongo_client.test_database
collection = db.test_collection

@app.get("/test")
async def test_endpoint():
    return 'OK'

@app.get("/", response_class=HTMLResponse)
async def liff_html(request: Request):
    data = await collection.find_one({"your_query_criteria": "your_value"})
    return templates.TemplateResponse("index.html", context={"request": request, "data": data})