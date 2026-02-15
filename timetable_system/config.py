import os

# Database Path
DB_PATH = os.path.join(os.getcwd(), "timetable.db")
DB_URL = f"sqlite:///{DB_PATH}"

# Global Config
MAX_ATTEMPTS = 500
