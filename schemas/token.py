from pydantic import BaseModel
from typing import Optional
from fastapi.security import OAuth2PasswordBearer


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")