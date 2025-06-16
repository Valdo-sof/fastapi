from fastapi import FastAPI, Body, Path, Query, Depends, Form, Header, Cookie
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse, FileResponse, Response
from pydantic import BaseModel, Field, validator
from typing import Optional, List
import datetime
from src.routers.movie_router import movie_router
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
import os
from fastapi import HTTPException
from jose import jwt, JWTError

#ejemplo de dependencias que pueeden ser usadas globalmente en cualquier parteb de la APP 
def dependency1():
    print("Dependency 1 is working")
def dependency2():
    print("Dependency 2 is working")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")    


app = FastAPI(dependencies=[Depends(dependency1), Depends(dependency2)])

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

users = {
    "Osvaldo": {"username":"Osvaldo", "email":"valdo@gmail.com", "password":"1234"},
    "Karla": {"username":"Karla", "email":"karla@gmail.com", "password":"4321"},
}

def encode_token(payload: dict) -> str:
    # This is a placeholder for token encoding logic
    token=jwt.encode(payload, "mysecretkey", algorithm="HS256")
    return token
def decode_token(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    # This is a placeholder for token decoding logic
    data=jwt.decode(token, "mysecretkey", algorithms=["HS256"])
    user= users.get(data["username"])
    return user

@app.post("/token", tags=["Authentication"])
def login(form_data: Annotated[OAuth2PasswordRequestForm,Depends()]):
    user= users.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token= encode_token({"username": user["username"], "email": user["email"]})
    return {"access_token": token, "token_type": "bearer"}

def get_headers(
        access_token: Annotated[str | None,  Header()]= None,
        user_role: Annotated[str | None, Header()]= None,
):
    if access_token!= "mysecrettoken":
        raise HTTPException(status_code=403, detail="Invalid access token")
    return {
        "access_token": access_token,
        "user_role": user_role
    }

@app.get("/dashboard")
def dashboard(headers: Annotated[dict, Depends(get_headers)]):
    return {"acces_token": headers["access_token"], "user_role": headers["user_role"]}

@app.get("/users/profile", tags=["Authentication"])
def get_user_profile(my_user: Annotated[dict, Depends(decode_token)]):
    return my_user

@app.get("/example")
def example_cookies():
    response = JSONResponse(content={"message": "This is an example of setting cookies."})
    response.set_cookie(key="username", value="Osvaldo", expires=15)
    return response

@app.get("/cookies", tags=["Cookies"])
def get_cookies(username: str =Cookie()):
    return {"username": username}

@app.get("/", tags=["Home"])

def home(request: Request, my_user: Annotated[dict, Depends(decode_token)]):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Home Page", "message": "Welcome to FastAPI application!"})



@app.get("/get_file")
def get_file():
    return FileResponse("49631260.pdf", status_code=200, media_type="application/pdf", filename="49631260.pdf")

#def commons_params(start_date: str, end_date: str):
#    return {"start_date": start_date, "end_date": end_date}

class commonsDep:
    def __init__(self, start_date: str, end_date: str ) -> None:
        self.start_date = start_date
        self.end_date = end_date

@app.get("/users" )
def get_users(commons: commonsDep = Depends(commonsDep)):
    return f"{commons.start_date} and {commons.end_date}"


@app.get("/customers", tags=["Customers"])
def get_customers(commons: commonsDep = Depends(commonsDep)):
    return f"{commons.start_date} and {commons.start_date}"


app.include_router(prefix="/movies", router=movie_router)