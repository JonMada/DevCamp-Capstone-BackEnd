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
    cover_image: Optional[str] = None  # Este campo se convertirá a base64
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
        cover_image_base64 = None
        if obj.cover_image is not None:
            try:
                cover_image_base64 = base64.b64encode(obj.cover_image).decode('utf-8')
            except Exception as e:
                print(f"Error base64: {e}")


        obj_dict = obj.__dict__

        obj_dict['cover_image'] = cover_image_base64
        return super(Book, cls).from_orm(obj)
