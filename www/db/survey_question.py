from .base import Base
from .survey_answer_choice import SurveyAnswerChoice
from .survey_response_answer import SurveyResponseAnswer

from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import VARCHAR, CHAR, BIGINT


class SurveyQuestion(Base):
    survey_id = Column(BIGINT, ForeignKey('survey.id'))
    question_text = Column(VARCHAR(255), default='')
    type = Column(CHAR(1), default='')

    answer_choices = relationship(SurveyAnswerChoice, backref='survey_question')
    survey_response_answers = relationship(SurveyResponseAnswer, backref='survey_question')