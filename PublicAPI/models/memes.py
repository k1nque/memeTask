from sqlalchemy.orm import Mapped
from .base import Base


class Memes(Base):
    __tablename__ = "memes"
    descriprion: Mapped[str]