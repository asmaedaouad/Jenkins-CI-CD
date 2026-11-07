@'
import unittest
from app import app


class TestApp2(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_sum_negative_numbers(self):
        response = self.client.post('/sum', data={'a': '-2', 'b': '-3'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'-5.0', response.data)

    def test_sum_decimals(self):
        response = self.client.post('/sum', data={'a': '1.5', 'b': '2.25'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'3.75', response.data)

    def test_hello_strips_spaces(self):
        response = self.client.post('/hello', data={'username': '   '})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello there', response.data)

    def test_unknown_route_returns_404(self):
        response = self.client.get('/inexistant')
        self.assertEqual(response.status_code, 404)

    def test_get_not_allowed_on_sum(self):
        response = self.client.get('/sum')
        self.assertEqual(response.status_code, 405)


if __name__ == "__main__":
    unittest.main()
'@ | Set-Content -Encoding ascii test_app_2.py