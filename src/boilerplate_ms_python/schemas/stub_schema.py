from pydantic import BaseModel


class StubSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
