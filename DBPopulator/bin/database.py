from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
import os
import datetime

#db_server = os.environ['DB_SERVER']
#db_name = os.environ['DB_NAME']
#db_user = os.environ['DB_USER']
#db_pwd = os.environ['DB_PWD']
Base = declarative_base()


def create_tables(engine):
    Base.metadata.create_all(engine)


def drop_tables(engine):
    Base.metadata.drop_all(engine)


def create_session(engine):
    return Session(bind=engine)
    

class ApiContent(Base):
    __tablename__ = 'API_CONTENT'
    id = Column(Integer, primary_key=True)
    content = Column(Text)    

    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.id} content={self.content}'

class RoomUsers(Base):
    __tablename__ = 'ROOM_USERS'
    id = Column(Integer, primary_key=True)
    room_id = Column(String)
    upn = Column(String)