from fastapi import APIRouter, Depends, HTTPException

# Models
from models.tea import TeaModel
from models.comment import CommentModel
from models.user import UserModel

# Serializers & Validations
from serializers.comment import CommentSchema, CreateCommentSchema, UpdateCommentSchema
from typing import List

# DB
from sqlalchemy.orm import Session
from database import get_db

# Auth
from dependencies.get_current_user import get_current_user

router = APIRouter()

@router.get("/teas/{tea_id}/comments", response_model=List[CommentSchema])
def get_comments_for_tea(tea_id: int, db: Session = Depends(get_db)):
    tea = db.query(TeaModel).filter(TeaModel.id == tea_id).first()
    if not tea:
        raise HTTPException(status_code=404, detail="Tea not found")
    return tea.comments

@router.get("/comments/{comment_id}", response_model=CommentSchema)
def get_comment_by_id(comment_id: int,  db: Session = Depends(get_db)):
    comment = db.query(CommentModel).filter(CommentModel.id == comment_id).first()

    if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")

    return comment

# any logged in user can create a comment
@router.post("/teas/{tea_id}/comments", response_model=CommentSchema, status_code=201)
def create_comment(tea_id: int, comment: CreateCommentSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    tea = db.query(TeaModel).filter(TeaModel.id == tea_id).first()

    if not tea:
        raise HTTPException(status_code=404, detail="Tea not found")

    # the logged in user becomes the comment's owner
    new_comment = CommentModel(**comment.dict(), tea_id=tea_id, user_id=current_user.id)

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment

# only the comment's owner can update it
@router.put("/comments/{comment_id}", response_model=CommentSchema)
def update_comment(comment_id: int, comment: UpdateCommentSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
  db_comment = db.query(CommentModel).filter(CommentModel.id == comment_id).first()

  if not db_comment:
    raise HTTPException(status_code=404, detail="Comment not found")

  # check if the current user wrote the comment
  if db_comment.user_id != current_user.id:
    raise HTTPException(status_code=403, detail="Operation forbidden")

  comment_data = comment.dict(exclude_unset=True)

  for key, val in comment_data.items():
      setattr(db_comment, key, val)

  db.commit()
  db.refresh(db_comment)

  return db_comment

# only the comment's owner can delete it
@router.delete("/comments/{comment_id}", status_code=204)
def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    db_comment = db.query(CommentModel).filter(CommentModel.id == comment_id).first()

    if not db_comment:
      raise HTTPException(status_code=404, detail="Comment not found")

    # check if the current user wrote the comment
    if db_comment.user_id != current_user.id:
      raise HTTPException(status_code=403, detail="Operation forbidden")

    db.delete(db_comment)
    db.commit()

    return None