from datetime import date

from pydantic import BaseModel


class PostSchema(BaseModel):
     title: str
     publication_date: date
     story: str 
     # images: 

     class Config:
        from_attributes = True