from fastapi import APIRouter, status, Response, Depends
from typing import Optional, List
from sqlalchemy.orm import Session

from schemas import UserBase, UserDisplay
from db.database import get_db
from db import db_user


router = APIRouter(prefix='/user', tags=['user'])

@router.post('/create', response_model = UserDisplay)
def create_user(request: UserBase, db:Session = Depends(get_db)):
    return db_user.create_user(db, request)


@router.get('/',response_model = List[UserDisplay])
def get_all_users(db:Session = Depends(get_db)):
    return db_user.get_all_users(db)


@router.get('/{id}',response_model = UserDisplay)
def get_user(id: int, db:Session = Depends(get_db)):
    return db_user.get_user(db, id)


@router.put('/{id}/update')
def update_user(id: int, request: UserBase, db:Session = Depends(get_db)):
    return db_user.update_user(db, id, request)


@router.delete('/{id}/delete')
def delete_user(id: int, db:Session = Depends(get_db)):
    return db_user.delete_user(db, id)