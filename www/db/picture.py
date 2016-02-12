from .base import Base
from .user import User

from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column
from sqlalchemy.types import BLOB


class Picture(Base):
    picture = Column(BLOB)

    users = relationship(User, backref='picture')