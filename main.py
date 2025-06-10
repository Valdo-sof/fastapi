from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse, FileResponse
from pydantic import BaseModel, Field, validator
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
    @validator("title")
    def validate_title(cls, value):
        if len(value) < 5:  
                raise ValueError("Title must be at least 5 characters long")
        if len(value) > 20:
                raise ValueError("Title must be at most 20 characters long")
        return value  

class MovieUpdate(BaseModel):
    title: str
    year: int
    genre: list
    rating: float
    director: str    

@app.get("/", tags=["Home"])

def home():
    return PlainTextResponse("Welcome to the FastAPI application!", status_code=200)

movies:List[Movie] = []

@app.get("/movies", tags=["Movies"], status_code=200, response_description=" Success List of movies")

def get_movies()-> List[Movie]:
    content= [movie.model_dump() for movie in movies]
    return  JSONResponse(content=content, status_code=200)

@app.get("/movies/{id}", tags=["Movies"])

def get_movie(id: int = Path(gt=0))-> Movie | dict:
    for movie in movies:
        if movie.id == id:

            return JSONResponse(content=movie.model_dump(), status_code=200)

    return JSONResponse(content={"message": "Movie not found"}, status_code=404)


@app.get("/movies/", tags=["Movies"])

def get_movie_by_category(gener: str = Query(min_length=5, max_length=20))-> List[Movie] | dict:
    result = []
    for movie in movies:
        if gener in movie.genre:
            result.append(movie)
    
    if not result:
        return JSONResponse(content={"message": "No movies found in this genre"}, status_code=404)
    
    return JSONResponse(content=[movie.model_dump() for movie in result], status_code=200)


@app.post("/movies/", tags=["Movies"])

def create_movie(movie: MovieCreate)-> List[Movie]:
    movies.append(movie)
    content= [movie.model_dump() for movie in movies]
    return  JSONResponse(content=content, status_code=201)

    
@app.put("/movies/{id}", tags=["Movies"])

def update_movie(id: int, movie: MovieUpdate)-> List[Movie]:
    for item in movies:
        if item.id == id:
            item.title = movie.title
            item.year = movie.year
            item.genre = movie.genre
            item.rating = movie.rating
            item.director = movie.director
        content= [movie.model_dump() for movie in movies]
        return  JSONResponse(content=content, status_code=200)
    return JSONResponse(content={"message": "Movie not found"}, status_code=404)

@app.delete("/movies/{id}", tags=["Movies"])
def delete_movie(id: int= Path(gt=0))-> List[Movie]:
    for movie in movies:
        if movie.id == id:
            movies.remove(movie)
        content= [movie.model_dump() for movie in movies]
        return  JSONResponse(content=content, status_code=200)


    return JSONResponse(content={"message": "Movie not found"}, status_code=404)

@app.get("/get_file")
def get_file():
    return FileResponse("49631260.pdf", status_code=200, media_type="application/pdf", filename="49631260.pdf")