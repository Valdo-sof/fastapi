from fastapi import FastAPI

app = FastAPI()

app.title = "FastAPI application"
app.description = "This is a simple API to FastAPI usage."
app.version = "0.1.0"

@app.get("/", tags=["Home"])

def home():
    return {"message": "Hello World, write your first API with FastAPI!"}

@app.get("/movies", tags=["Home"])

def hometwo():
    return {"message": "Hello World, write your first API with FastAPI!"}