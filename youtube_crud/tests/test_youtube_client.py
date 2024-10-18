import unittest
from youtube_crud.youtube_client import YouTubeClient

class TestYouTubeClient(unittest.TestCase):

    def test_read_video(self):
        client = YouTubeClient("AIzaSyAoJkXMU9V8t6Rn3Y_b_UkignLNAI305sk")
        result = client.read_video("Kz6IlDCyOUY")
        self.assertIn('items', result)

if __name__ == '__main__':
    unittest.main()
