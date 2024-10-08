from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True



class BookBase(BaseModel):
    title: str
    author: str
    year_published: Optional[int] = None
    cover_image: str  
    summary: Optional[str] = None
    review: Optional[str] = None
    rating: Optional[int] = None

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
   
