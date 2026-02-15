from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from timetable_system.models import Timetable, TimetableEntry

class TimetableManager:
    def __init__(self, db: Session):
        self.db = db

    def get_all_timetables(self):
        """Retrieve all saved timetables."""
        return self.db.query(Timetable).all()

    def get_timetable_by_name(self, name: str):
        """Retrieve a timetable by its unique name."""
        return self.db.query(Timetable).filter(Timetable.name == name).first()

    def create_timetable(self, name: str, entries_data: dict, periods: int):
        """
        Save a generated timetable.
        entries_data format: { "12B": ["MATH", "PHY", ...], "12N": [...] }
        """
        timetable = Timetable(name=name)
        self.db.add(timetable)
        
        try:
            self.db.flush() # Get ID before committing
        except IntegrityError:
            self.db.rollback()
            raise ValueError(f"Timetable with name '{name}' already exists.")

        for class_name, subjects in entries_data.items():
            for i, subject in enumerate(subjects):
                if i >= periods: break
                entry = TimetableEntry(
                    timetable_id=timetable.id,
                    period_index=i,
                    class_name=class_name,
                    subject=subject
                )
                self.db.add(entry)
        
        self.db.commit()
        return timetable

    def delete_timetable(self, name: str):
        """Delete a timetable by name."""
        timetable = self.get_timetable_by_name(name)
        if timetable:
            self.db.delete(timetable)
            self.db.commit()
            return True
        return False
