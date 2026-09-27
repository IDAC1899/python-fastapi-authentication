from pydantic import BaseModel
# these imports are fromn Python
from typing import Optional, List
from .comment import CommentSchema

class TeaSchema(BaseModel):
  id: Optional[int] = True
  name: str
  in_stock: bool
  rating: int
  comments: List[CommentSchema]

# These are Schema Validations for the req.body on Create and Update
class CreateTeaSchema(BaseModel):
  name: str
  in_stock: bool
  rating: int

class UpdateTeaSchema(BaseModel):
  name: str
  in_stock: bool
  rating: int