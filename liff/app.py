from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
#from pymongo import MongoClient

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

#client = MongoClient("mongodb://mongodb:27017/")
#db = client["test_database"] #database name
#collection = db["env_device_data"] #collection name

@app.get("/test")
async def test_endpoint():
    return 'OK'

@app.get("/", response_class=HTMLResponse)
async def liff_html(request: Request):
    data = requests.post("http://iot:8000/api/front/environ_data", json={"device_id": "c466"})
    return templates.TemplateResponse("index.html", context={"request": request, "data": data})
