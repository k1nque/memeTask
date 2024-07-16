from pydantic import BaseModel, ConfigDict


class MemeBase(BaseModel):
    description: str

class MemeCreate(MemeBase):
    pass

class Meme(MemeBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
