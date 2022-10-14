from sqlalchemy import create_engine, Integer, String, Boolean, DateTime, Column
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

engine = create_engine('sqlite:///tasks.db', echo=True)

session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base() 

"""
***Database representation layout***

  class Task:
    id - int
    content - str
    date_added - datetime
    is_completed - boolean

"""
class Task(Base):  
  
  __tablename__ = 'tasks' # The database name

  id = Column(Integer(), primary_key=True)
  content = Column(String(500), nullable=False)
  date_added = Column(DateTime(), default=datetime.utcnow())
  is_completed = Column(Boolean(), default=False)

  def __repr__(self):
    return f'<Task {self.id}>'

# Note -> The Task class contents == metadata 

Base.metadata.create_all(bind=engine) 



