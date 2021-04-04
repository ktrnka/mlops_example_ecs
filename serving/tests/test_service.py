import unittest

from serving.app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


class BasicTests(unittest.TestCase):
    def test_valid_prediction(self):
        response = client.post("/predict", json={"text": "hi mom"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("category", response.json())

    def test_health(self):
        response = client.get("/health")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
