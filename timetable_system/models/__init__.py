from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from timetable_system.config import DB_URL
from .timetable import Base, Timetable, TimetableEntry

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
