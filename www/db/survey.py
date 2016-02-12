from .base import Base
from .survey_question import SurveyQuestion
from .survey_response import SurveyResponse

from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column
from sqlalchemy.types import VARCHAR


class Survey(Base):
    name = Column(VARCHAR(255), default='')

    survey_questions = relationship(SurveyQuestion, backref='survey')
    survey_responses = relationship(SurveyResponse, backref='survey')