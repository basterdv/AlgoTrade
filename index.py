from fastapi import FastAPI
from starlette.responses import HTMLResponse
from pages import router as router_pages

app = FastAPI()


@app.get("/")
async def main():
    page = "<h1>Hello World!</h1>"  # текст ответа сервера
    return HTMLResponse(content=page)
