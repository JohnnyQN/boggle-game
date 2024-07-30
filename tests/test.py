from unittest import TestCase
from app import app
from flask import session

class FlaskTests(TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_index(self):
        """Test that the index route displays the game board."""
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Boggle Game', response.data)

    def test_check_word(self):
        """Test the /check-word route."""
        with self.client:
            response = self.client.post('/check-word', json={'word': 'TEST'})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'not-word', response.data)  # Adjust based on the actual result

    def test_end_game(self):
        """Test the /end-game route."""
        with self.client:
            response = self.client.post('/end-game', json={'score': 10})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'games_played', response.data)
            self.assertIn(b'highest_score', response.data)
