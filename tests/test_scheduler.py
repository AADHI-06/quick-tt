import unittest
from timetable_system.services.scheduler import TimetableScheduler

class TestScheduler(unittest.TestCase):
    def test_basic_schedule(self):
        periods = 4
        data = {
            "12A": ["MATH", "MATH", "PHY", "CHEM"],
            "12B": ["PHY", "CHEM", "MATH", "BIO"]
            # 12A: M, M, P, C
            # 12B: P, C, M, B
        }
        # In this simple case, a valid schedule exists (e.g. 12A: M, M, P, C | 12B: P, C, M, B)
        # But wait, 12A has MATH at index 0, 12B has PHY. No clash.
        # 12A has MATH at index 1, 12B has CHEM. No clash.
        # 12A has PHY at index 2, 12B has MATH. No clash.
        # ...
        
        # Let's try a case that MIGHT clash if not shuffled right.
        # Actually random shuffling will eventually find a solution.
        
        scheduler = TimetableScheduler(data, periods)
        result = scheduler.solve()
        
        self.assertIsNotNone(result)
        self.assertEqual(len(result["12A"]), periods)
        
        # Verify no clashes
        for i in range(periods):
            slot = [result[cls][i] for cls in data]
            self.assertEqual(len(slot), len(set(slot)), f"Clash found at period {i}: {slot}")

    def test_impossible_schedule(self):
        periods = 2
        data = {
            "12A": ["MATH", "MATH"],
            "12B": ["MATH", "MATH"]
        }
        # Both classes MUST have MATH in both periods.
        # Period 0: 12A=MATH, 12B=MATH -> CLASH!
        
        scheduler = TimetableScheduler(data, periods)
        result = scheduler.solve()
        
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
