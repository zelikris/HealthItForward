import re
import time
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.schema import Column
from sqlalchemy.types import BigInteger

class Base(object):

    @declared_attr
    def __tablename__(cls):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', cls.__name__)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def __current_timestamp__():
        return int(time.time())

    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}

    id = Column(BigInteger, primary_key=True)
    time_created = Column(BigInteger, default=__current_timestamp__)
    time_updated = Column(BigInteger, default=__current_timestamp__, onupdate=__current_timestamp__)

Base = declarative_base(cls=Base)
