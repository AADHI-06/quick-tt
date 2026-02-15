from fastapi.testclient import TestClient
from api.main import app
import unittest

client = TestClient(app)

class TestAPI(unittest.TestCase):
    def test_generate_timetable(self):
        payload = {
            "periods": 2,
            "classes": {
                "12A": ["MATH", "PHY"],
                "12B": ["BIO", "CHEM"]
            }
        }
        response = client.post("/generate", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("12A", data)
        self.assertEqual(len(data["12A"]), 2)

    def test_create_and_list_timetables(self):
        # 1. Generate local schedule
        schedule = {
            "12A": ["MATH", "PHY"],
            "12B": ["BIO", "CHEM"]
        }
        
        # 2. Save it
        payload = {
            "name": "APITestTable",
            "periods": 2,
            "entries": schedule
        }
        response = client.post("/timetables", json=payload)
        if response.status_code == 400:
            # Already exists from previous run? Try a new name
             payload["name"] = "APITestTable_New"
             response = client.post("/timetables", json=payload)

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], payload["name"])
        
        # 3. List
        response = client.get("/timetables")
        self.assertEqual(response.status_code, 200)
        timetables = response.json()
        self.assertTrue(any(t["name"] == payload["name"] for t in timetables))

if __name__ == "__main__":
    unittest.main()
