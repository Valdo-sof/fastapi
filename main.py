from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

app.title = "FastAPI application"
app.description = "This is a simple API to FastAPI usage."
app.version = "0.1.0"

class Movie(BaseModel):
    id: int
    title: str
    year: int
    genre: list
    rating: float
    director: str

class MovieUpdate(BaseModel):
    title: str
    year: int
    genre: list
    rating: float
    director: str    

@app.get("/", tags=["Home"])

def home():
    return {"message": "Hello World, write your first API with FastAPI!"}

movies=[
  {
    "id": 1,
    "title": "The Shawshank Redemption",
    "year": 1994,
    "genre": ["Drama"],
    "rating": 9.3,
    "director": "Frank Darabont"
  },
  {
    "id": 2,
    "title": "The Godfather",
    "year": 1972,
    "genre": ["Crime", "Drama"],
    "rating": 9.2,
    "director": "Francis Ford Coppola"
  },
  {
    "id": 3,
    "title": "The Dark Knight",
    "year": 2008,
    "genre": ["Action", "Crime", "Drama"],
    "rating": 9.0,
    "director": "Christopher Nolan"
  },
  {
    "id": 4,
    "title": "Pulp Fiction",
    "year": 1994,
    "genre": ["Crime", "Drama"],
    "rating": 8.9,
    "director": "Quentin Tarantino"
  },
  {
    "id": 5,
    "title": "Inception",
    "year": 2010,
    "genre": ["Action", "Adventure", "Sci-Fi"],
    "rating": 8.8,
    "director": "Christopher Nolan"
  }
]


@app.get("/movies", tags=["Movies"])

def get_movies()-> List[Movie]:
    return movies

@app.get("/movies/{id}", tags=["Movies"])

def get_movie(id: int)-> Movie:
    for movie in movies:
        if movie["id"] == id:
            return movie

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

def create_movie(movie: Movie):
    new_movie = movie.dict()
    movies.append(new_movie)
    return movies
    
@app.put("/movies/{id}", tags=["Movies"])

def update_movie(id: int, movie: MovieUpdate)-> List[Movie]:
    for item in movies:
        if item["id"] == id:
            item["title"] = movie.title
            item["year"] = movie.year
            item["genre"] = movie.genre
            item["rating"] = movie.rating
            item["director"] = movie.director
            return movies

    return {"message": "Movie not found"}

@app.delete("/movies/{id}", tags=["Movies"])
def delete_movie(id: int)-> List[Movie]:
    for movie in movies:
        if movie["id"] == id:
            movies.remove(movie)
            return movies

    return {"message": "Movie not found"}