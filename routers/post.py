from fastapi import APIRouter, status, Response, Depends, HTTPException, File
from typing import Optional, List
from fastapi.datastructures import UploadFile
from sqlalchemy.orm import Session
import random, string, shutil

from schemas import PostBase, PostDisplay, User
from db.database import get_db
from db import db_post
from auth.oauth2 import get_current_user


router = APIRouter(prefix='/post', tags=['post'])

image_url_types = ['absolute', 'relative',]

@router.post('/', response_model = PostDisplay)
def create_post(request: PostBase, db:Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not request.image_url_type in image_url_types:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Parameter image_url_type can only take values 'absolute' or 'relative'."
        )
    return db_post.create_post(db, request)

@router.get('/all',response_model = List[PostDisplay])
def get_all_posts(db:Session = Depends(get_db)):
    return db_post.get_all_posts(db)


@router.get('/{id}',) # response_model = PostDisplay)
def get_post(id: int, db:Session = Depends(get_db)):
    return {
        'data': db_post.get_post(db, id),
    }

@router.post('/image')
def upload_image(image: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    letters = string.ascii_letters
    rand_str = ''.join(random.choice(letters) for i in range(8))
    new = f'_{rand_str}.'
    filename = new.join(image.filename.rsplit('.', 1))
    path = f'images/{filename}'

    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)

    return {'filename': path}

@router.delete('/{id}/delete')
def delete_post(id: int, db:Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db_post.delete_post(db, id, current_user.id)
