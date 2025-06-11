from fastapi import FastAPI, Body, Path, Query
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse, FileResponse, Response
from pydantic import BaseModel, Field, validator
from typing import Optional, List
import datetime
from src.routers.movie_router import movie_router
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os


app = FastAPI()

app.title = "FastAPI application"
app.description = "This is a simple API to FastAPI usage."
app.version = "0.1.0"

@app.middleware("http")
async def http_error_handler(request, call_next)-> JSONResponse | Response:
    print("Middleware is working")
    return await call_next(request)

statict_path = os.path.join(os.path.dirname(__file__), "static/")
templates_path = os.path.join(os.path.dirname(__file__), "templates/")

app.mount("/static", StaticFiles(directory=statict_path), name="static")
templates = Jinja2Templates(directory=templates_path)




@app.get("/", tags=["Home"])

def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Home Page", "message": "Welcome to FastAPI application!"})



@app.get("/get_file")
def get_file():
    return FileResponse("49631260.pdf", status_code=200, media_type="application/pdf", filename="49631260.pdf")


app.include_router(prefix="/movies", router=movie_router)