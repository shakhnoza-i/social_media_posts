from sqlalchemy.orm.session import Session
from fastapi import HTTPException, status
import datetime

from schemas import CommentBase
from db.models import DbComment


def create(db:Session, request:CommentBase): 
    new_comment = DbComment(
        text = request.text,
        username = request.username,
        post_id = request.post_id,
        timestamp = datetime.datetime.now(),
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

def get_all(db: Session, post_id: int):
    return db.query(DbComment).filter(DbComment.id == post_id).all()

def get(db: Session, id:int):
    comment = db.query(DbComment).filter(DbComment.id == id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail = f'Comment with id {id} not found')
    return comment

def delete(db: Session, id:int, user_id: int):
    comment = db.query(DbComment).filter(DbComment.id == id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail = f'Comment with id {id} not found')
    if comment.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail = f'Only comment creator can delete comment')
    db.delete(comment)
    db.commit()
    return f"Comment with id {id} has been deleted"
