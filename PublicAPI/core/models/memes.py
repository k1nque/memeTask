from fileinput import filename
from sqlalchemy.orm import Mapped
from .base import Base


class Meme(Base):
    __tablename__ = "memes"
    description: Mapped[str]
    filename: Mapped[str]