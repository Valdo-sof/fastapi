from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional, List
import datetime

app = FastAPI()

app.title = "FastAPI application"
app.description = "This is a simple API to FastAPI usage."
app.version = "0.1.0"

class Movie(BaseModel):
    id: int
    title: str
    year: int
    genre: list [str]
    rating: float
    director: str

class MovieCreate(BaseModel):
    id: int
    title: str = Field(min_length=5, max_length=20, default="Default Title")  # Assuming a movie title is between 5 and 20 characters
    year: int = Field(gt=1888, le=datetime.date.today().year, default=datetime.date.today().year)  # Movies started being made in 1888
    genre: list = Field(min_length=1, max_length=5)  # Assuming a movie can have 1 to 5 genres
    rating: float = Field(gt=0, le=10, default=0.1)  # Assuming rating is out of 10
    director: str = Field(min_length=4, max_length=50, default="none")  # Assuming a director's name is between 3 and 50 characters 

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 6,
                "title": "New Movie",
                "year": 2025,
                "genre": ["Action", "Adventure"],
                "rating": 8.5,
                "director": "John Doe"
            }
        }
    } 

class MovieUpdate(BaseModel):
    title: str
    year: int
    genre: list
    rating: float
    director: str    

@app.get("/", tags=["Home"])

def home():
    return {"message": "Hello World, write your first API with FastAPI!"}

movies:List[Movie] = []

@app.get("/movies", tags=["Movies"])

def get_movies()-> List[Movie]:
    return [movie.model_dump() for movie in movies]

@app.get("/movies/{id}", tags=["Movies"])

def get_movie(id: int)-> Movie:
    for movie in movies:
        if movie["id"] == id:
            return movie.model_dump()

    return {"message": "Movie not found"}


@app.get("/movies/", tags=["Movies"])

def get_movie_by_category(gener: str)-> List[Movie]:
    result = []
    for movie in movies:
        if gener in movie["genre"]:
            result.append(movie)
    
    if not result:
        return {"message": "No movies found for this genre"}
    
    return result


@app.post("/movies/", tags=["Movies"])

def create_movie(movie: MovieCreate)-> List[Movie]:
    movies.append(movie)
    return [movie.model_dump() for movie in movies]
    
@app.put("/movies/{id}", tags=["Movies"])

def update_movie(id: int, movie: MovieUpdate)-> List[Movie]:
    for item in movies:
        if item["id"] == id:
            item["title"] = movie.title
            item["year"] = movie.year
            item["genre"] = movie.genre
            item["rating"] = movie.rating
            item["director"] = movie.director
            return [movie.model_dump() for movie in movies]

    return {"message": "Movie not found"}

@app.delete("/movies/{id}", tags=["Movies"])
def delete_movie(id: int)-> List[Movie]:
    for movie in movies:
        if movie["id"] == id:
            movies.remove(movie)
            return [movie.model_dump() for movie in movies]

    return {"message": "Movie not found"}