from pydantic import BaseModel, ConfigDict


class MemeBase(BaseModel):
    description: str
    filename: str

class MemeCreate(MemeBase):
    pass


class MemeUpdate(MemeBase):
    pass


class MemeUpdatePartitial(MemeUpdate):
    description: str | None = None
    filename: str | None = None
    

class Meme(MemeBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
