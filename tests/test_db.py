import unittest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from timetable_system.models.timetable import Base, Timetable
from timetable_system.repositories.timetable_manager import TimetableManager

class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Use in-memory SQLite for testing
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.db = self.Session()
        self.tm = TimetableManager(self.db)

    def tearDown(self):
        self.db.close()

    def test_create_and_retrieve_timetable(self):
        name = "TestTable1"
        periods = 2
        entries_data = {
            "12A": ["MATH", "PHY"],
            "12B": ["BIO", "CHEM"]
        }
        
        # Create
        t = self.tm.create_timetable(name, entries_data, periods)
        self.assertIsNotNone(t.id)
        self.assertEqual(t.name, name)
        
        # Retrieve
        t_fetched = self.tm.get_timetable_by_name(name)
        self.assertEqual(t_fetched.id, t.id)
        self.assertEqual(len(t_fetched.entries), 4) # 2 periods * 2 classes
        
        # Delete
        success = self.tm.delete_timetable(name)
        self.assertTrue(success)
        self.assertIsNone(self.tm.get_timetable_by_name(name))

if __name__ == '__main__':
    unittest.main()
