from .base import Base

from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import BIGINT, VARCHAR


class SurveyResponseAnswer(Base):
    survey_response_id = Column(BIGINT, ForeignKey('survey_response.id'))
    survey_question_id = Column(BIGINT, ForeignKey('survey_question.id'))
    response_value = Column(VARCHAR(255), default='')