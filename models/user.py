from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt

# Import the secret from the environment file
from config.environment import JWT_SECRET

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserModel(BaseModel):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)  # Each username must be unique
    email = Column(String, unique=True)  # Each email must be unique
    password = Column(String, nullable=True)

    comments = relationship('CommentModel', back_populates="user")

    def set_password(self, plain_txt_password: str):
        self.password = pwd_context.hash(plain_txt_password)

    # checks a plain text password against the stored hashed password
    def verify_password(self, plain_txt_password: str) -> bool:
        return pwd_context.verify(plain_txt_password, self.password)

    # builds and signs a jwt token containing this user's id
    def generate_token(self):
        payload = {
            "exp": datetime.now(timezone.utc) + timedelta(days=1),  # expiration time (1 day)
            "iat": datetime.now(timezone.utc),  # issued at time
            # pyjwt requires sub to be a string
            "sub": str(self.id),  # subject - the user id
        }

        token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

        return token