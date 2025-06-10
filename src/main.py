from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse, FileResponse
from pydantic import BaseModel, Field, validator
from typing import Optional, List
import datetime
from src.routers.movie_router import movie_router


app = FastAPI()

app.title = "FastAPI application"
app.description = "This is a simple API to FastAPI usage."
app.version = "0.1.0"




@app.get("/", tags=["Home"])

def home():
    return PlainTextResponse("Welcome to the FastAPI application!", status_code=200)



@app.get("/get_file")
def get_file():
    return FileResponse("49631260.pdf", status_code=200, media_type="application/pdf", filename="49631260.pdf")


app.include_router(prefix="/movies", router=movie_router)