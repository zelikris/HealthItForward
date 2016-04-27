import config

import time

import re
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import BIGINT, VARCHAR, CHAR, TEXT
from sqlalchemy.types import BLOB

session = scoped_session(sessionmaker(bind=create_engine(config.db_url, echo=True)))


class Base(object):
    """Base object for all database classes."""

    @declared_attr
    def __tablename__(cls):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', cls.__name__)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def __current_timestamp__(self):
        return int(time.time())

    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}

    id = Column(BIGINT, primary_key=True)
    time_created = Column(BIGINT, default=__current_timestamp__)
    time_updated = Column(BIGINT, default=__current_timestamp__, onupdate=__current_timestamp__)


Base = declarative_base(cls=Base)


class SurveyAnswerChoice(Base):
    text = Column(VARCHAR(255), default='')
    survey_question_id = Column(BIGINT, ForeignKey('survey_question.id'))


class SurveyResponseAnswer(Base):
    survey_response_id = Column(BIGINT, ForeignKey('survey_response.id'))
    survey_question_id = Column(BIGINT, ForeignKey('survey_question.id'))
    response_value = Column(VARCHAR(255), default='')


class SurveyResponse(Base):
    user_id = Column(BIGINT, ForeignKey('user.id'))
    survey_id = Column(BIGINT, ForeignKey('survey.id'))

    survey_response_answers = relationship(SurveyResponseAnswer, backref='survey_response')


class SurveyQuestion(Base):
    survey_id = Column(BIGINT, ForeignKey('survey.id'))
    question_text = Column(VARCHAR(255), default='')
    type = Column(CHAR(1), default='')

    answer_choices = relationship(SurveyAnswerChoice, backref='survey_question')
    survey_response_answers = relationship(SurveyResponseAnswer, backref='survey_question')


class Survey(Base):
    name = Column(VARCHAR(255), default='')

    survey_questions = relationship(SurveyQuestion, backref='survey')
    survey_responses = relationship(SurveyResponse, backref='survey')


class User(Base):
    name = Column(VARCHAR(255), default='')
    email = Column(VARCHAR(255), default='')
    password_hash = Column(VARCHAR(255), default='')
    screen_name = Column(VARCHAR(255), default='')
    sex = Column(CHAR(1), default='')
    birthday = Column(CHAR(8), default='')
    picture_id = Column(BIGINT, ForeignKey('picture.id'))
    race = Column(CHAR(3), default='')
    intro = Column(TEXT, default='')
    city = Column(VARCHAR(255), default='')
    state = Column(CHAR(3), default='')
    country = Column(CHAR(3), default='')

    survey_responses = relationship(SurveyResponse, backref='user')


class Picture(Base):
    picture = Column(BLOB)

    users = relationship(User, backref='picture')
