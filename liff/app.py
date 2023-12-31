from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

client = MongoClient("mongodb://mongodb:27017/")
db = client["database_name"] # edit database name
collection = db["collection_name"] # edit collection name

@app.get("/test")
async def test_endpoint():
    return 'OK'

@app.get("/", response_class=HTMLResponse)
async def liff_html(request: Request):
    latest_entries = collection.find().sort("_id", -1).limit(15)
    data_to_render = [{"field1": entry["field1"], "field2": entry["field2"]} for entry in latest_entries]
    return templates.TemplateResponse("index.html", context={"request": request, "data": data_to_render})