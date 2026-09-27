from pydantic import BaseModel

class CommentSchema(BaseModel):
  id: int
  content: str

  class config:
    orm_mode = True


