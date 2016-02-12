from .base import Base
from .survey_response import SurveyResponse
from .user_location import UserLocation

from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import BIGINT, VARCHAR, CHAR


class User(Base):
    name = Column(VARCHAR(255), default='')
    email = Column(VARCHAR(255), default='')
    password_hash = Column(VARCHAR(255), default='')
    screen_name = Column(VARCHAR(255), default='')
    sex = Column(CHAR(1), default='')
    birthday = Column(CHAR(8), default='')
    picture_id = Column(BIGINT, ForeignKey('picture.id'))

    survey_responses = relationship(SurveyResponse, backref='user')
    locations = relationship(UserLocation, backref='user')