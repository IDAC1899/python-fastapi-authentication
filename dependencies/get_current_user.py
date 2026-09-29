from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from models.user import UserModel
from database import get_db
import jwt
from jwt import DecodeError, ExpiredSignatureError
from config.environment import JWT_SECRET

# reads the token from the "Authorization: Bearer <token>" header
http_bearer = HTTPBearer()

def get_current_user(db: Session = Depends(get_db), token: str = Depends(http_bearer)):

    try:
        # decode the token using our secret
        payload = jwt.decode(token.credentials, JWT_SECRET, algorithms=["HS256"])

        # find the user whose id is stored in the token
        user_in_database = db.query(UserModel).filter(UserModel.id == int(payload.get("sub"))).first()

        # no user with that id
        if not user_in_database:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    # token is invalid
    except DecodeError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Could not decode token: {str(e)}')

    # token is expired
    except ExpiredSignatureError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Token has expired')

    return user_in_database