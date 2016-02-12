from .base import Base
from .survey_response_answer import SurveyResponseAnswer

from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import BIGINT


class SurveyResponse(Base):
    user_id = Column(BIGINT, ForeignKey('user.id'))
    survey_id = Column(BIGINT, ForeignKey('survey.id'))

    survey_response_answers = relationship(SurveyResponseAnswer, backref='survey_response')