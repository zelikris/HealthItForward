from .base import Base

from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import VARCHAR, BIGINT


class SurveyAnswerChoice(Base):
    text = Column(VARCHAR(255), default='')
    survey_question_id = Column(BIGINT, ForeignKey('survey_question.id'))
