from fastapi import FastAPI, Body, Path, Query, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse, FileResponse
from pydantic import BaseModel, Field, validator
from typing import Optional, List
import datetime
from src.models.movie_model import Movie, MovieCreate, MovieUpdate

movie_router = APIRouter()

movies:List[Movie] = []


@movie_router.get("/", tags=["Movies"], status_code=200, response_description=" Success List of movies")
def get_movies()-> List[Movie]:
    content= [movie.model_dump() for movie in movies]
    return  JSONResponse(content=content, status_code=200)

@movie_router.get("/{id}", tags=["Movies"])
def get_movie(id: int = Path(gt=0))-> Movie | dict:
    for movie in movies:
        if movie.id == id:

            return JSONResponse(content=movie.model_dump(), status_code=200)

    return JSONResponse(content={"message": "Movie not found"}, status_code=404)


@movie_router.get("/gener", tags=["Movies"])
def get_movie_by_category(gener: str = Query(min_length=5, max_length=20))-> List[Movie] | dict:
    result = []
    for movie in movies:
        if gener in movie.genre:
            result.append(movie)
    
    if not result:
        return JSONResponse(content={"message": "No movies found in this genre"}, status_code=404)
    
    return JSONResponse(content=[movie.model_dump() for movie in result], status_code=200)


@movie_router.post("/", tags=["Movies"])
def create_movie(movie: MovieCreate)-> List[Movie]:
    movies.append(movie)
    content= [movie.model_dump() for movie in movies]
    return  JSONResponse(content=content, status_code=201)

    
@movie_router.put("/{id}", tags=["Movies"])
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

@movie_router.delete("/{id}", tags=["Movies"])
def delete_movie(id: int= Path(gt=0))-> List[Movie]:
    for movie in movies:
        if movie.id == id:
            movies.remove(movie)
        content= [movie.model_dump() for movie in movies]
        return  JSONResponse(content=content, status_code=200)


    return JSONResponse(content={"message": "Movie not found"}, status_code=404)