from pydantic import BaseModel
from .user import UserSchema

class CommentSchema(BaseModel):
  id: int
  content: str
  # the user who wrote the comment
  user: UserSchema

  class config:
    orm_mode = True

class CreateCommentSchema(BaseModel):
  content: str
class UpdateCommentSchema(BaseModel):
  content: str