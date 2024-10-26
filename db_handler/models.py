from sqlalchemy import Column, Integer, String, BigInteger, TIMESTAMP, DATE, Boolean
from sqlalchemy.ext.declarative import declarative_base
from utils.utils import get_now_time

Base = declarative_base()

class User(Base):
    __tablename__ = 'users_reg'

    user_id = Column(BigInteger, primary_key=True, autoincrement=False)
    full_name = Column(String)
    user_login = Column(String)
    refer_id = Column(BigInteger, nullable=True)
    count_refer = Column(Integer, default=0, server_default="0")
    date_reg = Column(TIMESTAMP, default=get_now_time())
    subscription_start = Column(DATE, nullable=True)
    subscription_end = Column(DATE, nullable=True)
    subscription_status = Column(Boolean, default=False)