from pydantic import BaseModel


class Postcreate(BaseModel):
    title: str
    content: str