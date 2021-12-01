from fastapi import FastAPI, status, Response, Request
from fastapi.responses import JSONResponse, PlainTextResponse, HTMLResponse
from fastapi.exceptions import HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.websockets import WebSocket
from fastapi.middleware.cors import CORSMiddleware

from db import models
from db.database import engine
from routers import user, post, comment
from auth import authentication


app = FastAPI()

app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(post.router)
app.include_router(comment.router)


@app.get('/hello/')
def root():
    return{'message': 'Hello world!'}


origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, # able to login and logout
    allow_methods=['*'],
    allow_headers=['*'],
)

models.Base.metadata.create_all(engine)

app.mount('/images', StaticFiles(directory="images"), name="images")
