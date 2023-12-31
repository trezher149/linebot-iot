from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
from datetime import datetime
import pytz

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
    environ_data = requests.post("http://iot:8000/api/front/environ_data", json={"device_id": "c466"})
    data = []
    for env in environ_data.json()["environ_data"]:
        date = datetime.fromisoformat(env["timestamp"])
        date = date.astimezone(pytz.timezone("Asia/Bangkok"))
        env["timestamp"] = date.strftime("%H:%M น. %d/%m/%Y")
        data.append(env)
    data.reverse()
    print(data)
    return templates.TemplateResponse("index.html", context={"request": request, "data": data})
