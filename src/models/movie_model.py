import datetime
from pydantic import BaseModel, Field, validator
from typing import List
from pydantic import BaseModel, Field, validator
from pydantic import BaseModel, Field, validator

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