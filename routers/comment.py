from fastapi import APIRouter, status, Response, Depends, HTTPException, File
from typing import Optional, List
from sqlalchemy.orm import Session

from schemas import CommentBase, User
from db.database import get_db
from db import db_comment
from auth.oauth2 import get_current_user


router = APIRouter(prefix='/comment', tags=['comment'])

@router.get('/all')
def get(post_id: int, db:Session = Depends(get_db)):
    return db_comment.get_all(db, post_id)

@router.post('/new')
def create(request: CommentBase, db:Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db_comment.create(db, request)
