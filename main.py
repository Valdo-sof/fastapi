from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

app.title = "FastAPI application"
app.description = "This is a simple API to FastAPI usage."
app.version = "0.1.0"

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


@app.get("/movies", tags=["Home"])

def get_movies():
    return movies

@app.get("/movies/{id}", tags=["Home"])

def get_movie(id: int):
    for movie in movies:
        if movie["id"] == id:
            return movie

    return {"message": "Movie not found"}


@app.get("/movies/", tags=["Home"])

def get_movie_by_category(gener: str):
    result = []
    for movie in movies:
        if gener in movie["genre"]:
            result.append(movie)
    
    if not result:
        return {"message": "No movies found for this genre"}
    
    return result
    