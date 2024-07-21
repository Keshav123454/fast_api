from pydantic import BaseModel, EmailStr, HttpUrl
from typing import List, Optional, Dict

class DestinationBase(BaseModel):
    url: HttpUrl
    http_method: str
    headers: Dict[str, str]

class DestinationCreate(DestinationBase):
    pass

class Destination(DestinationBase):
    id: int
    account_id: int

    class Config:
        orm_mode = True

class AccountBase(BaseModel):
    email: EmailStr
    name: str
    website: Optional[str]

class AccountCreate(AccountBase):
    pass

class Account(AccountBase):
    id: int
    app_secret_token: str
    destinations: List[Destination] = []

    class Config:
        orm_mode = True

