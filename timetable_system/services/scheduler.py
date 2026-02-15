import random
from timetable_system.config import MAX_ATTEMPTS

class TimetableScheduler:
    def __init__(self, data: dict, periods: int):
        self.data = data
        self.periods = periods
        self.classes = list(data.keys())

    def solve(self):
        """
        Attempts to generate a conflict-free schedule.
        Returns a dict of class -> [subjects] or None if failed.
        """
        for attempts in range(MAX_ATTEMPTS):
            # Shuffle subjects for each class initially
            shuffled_data = {
                cls: random.sample(subjects, len(subjects)) 
                for cls, subjects in self.data.items()
            }
            
            if self._is_valid_schedule(shuffled_data):
                return shuffled_data
        
        return None

    def _is_valid_schedule(self, schedule: dict) -> bool:
        """
        Validation:
        Check if any teacher/subject clashes exist in the same period across classes.
        Assumes 1 subject = 1 Teacher.
        """
        for i in range(self.periods):
            # Get subjects for all classes in period 'i'
            current_slot_subjects = []
            for cls in self.classes:
                if i < len(schedule[cls]):
                    current_slot_subjects.append(schedule[cls][i])
            
            # Check for duplicates (Teacher clash)
            # Filter out "FREE" or "LIBRARY" periods if they don't consume teacher resources?
            # For now, we assume ALL subjects are unique resources.
            if len(current_slot_subjects) != len(set(current_slot_subjects)):
                return False
        
        return True
