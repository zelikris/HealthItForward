from .base import Base

from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import BIGINT, VARCHAR, CHAR


class UserLocation(Base):
    user_id = Column(BIGINT, ForeignKey('user.id'))
    city = Column(VARCHAR(255), default='')
    state = Column(CHAR(3), default='')
    country = Column(CHAR(3), default='')