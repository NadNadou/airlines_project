import unittest
from app import app

class TestApp(unittest.TestCase):
    def test_get_countries(self):
        with app.test_client() as client:
            response = client.get('/countries')
            self.assertEqual(response.status_code, 200)

    def test_get_cities(self):
        pass