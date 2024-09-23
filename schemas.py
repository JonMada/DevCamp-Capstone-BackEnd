from pydantic import BaseModel
from typing import Optional
import base64

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
    cover_image: Optional[str] = None 
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
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        obj_dict = obj.__dict__.copy()

        if obj.cover_image is not None and isinstance(obj.cover_image, bytes):
            
            obj_dict['cover_image'] = base64.b64encode(obj.cover_image).decode('utf-8')

        return super(Book, cls).parse_obj(obj_dict)