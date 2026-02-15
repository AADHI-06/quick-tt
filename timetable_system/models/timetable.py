from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class Timetable(Base):
    __tablename__ = 'timetables'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to entries
    entries = relationship("TimetableEntry", back_populates="timetable", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Timetable(name='{self.name}')>"

class TimetableEntry(Base):
    __tablename__ = 'timetable_entries'

    id = Column(Integer, primary_key=True)
    timetable_id = Column(Integer, ForeignKey('timetables.id'), nullable=False)
    period_index = Column(Integer, nullable=False)  # 0-indexed period number
    class_name = Column(String(20), nullable=False) # e.g., "12B", "11A"
    subject = Column(String(50), nullable=False)

    timetable = relationship("Timetable", back_populates="entries")

    def __repr__(self):
        return f"<Entry({self.class_name}, Period {self.period_index}: {self.subject})>"
