import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestAPI(unittest.TestCase):

    def test_fetch(self):
        r = client.post("/waluty/fetch")
        self.assertEqual(r.status_code, 200)

    def test_get_all(self):
        r = client.get("/waluty")
        self.assertEqual(r.status_code, 200)

    def test_filter_year(self):
        r = client.get("/waluty?year=2026")
        self.assertEqual(r.status_code, 200)

    def test_filter_month(self):
        r = client.get("/waluty?year=2026&month=6")
        self.assertEqual(r.status_code, 200)

    def test_filter_day(self):
        r = client.get("/waluty?year=2026&month=6&day=5")
        self.assertEqual(r.status_code, 200)