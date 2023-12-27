from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/test")
async def test_endpoint():
    return 'OK'

@app.get("/", response_class=HTMLResponse)
async def liff_html(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})