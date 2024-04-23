from datetime import date
from typing import Annotated

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from pydantic import BaseModel, Field
import requests


app = FastAPI() # создаем экземпляр приложения через конструктор



@app.get("/")
async def get_root():
    page = "<h1>Hello World!</h1>" # текст ответа сервера
    return HTMLResponse(content=page)