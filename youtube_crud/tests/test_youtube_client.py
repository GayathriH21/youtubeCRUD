import unittest
from youtube_crud.youtube_client import YouTubeClient

class TestYouTubeClient(unittest.TestCase):
    def setUp(self):
        # Initialize the YouTube client with your API key
        self.client = YouTubeClient("AIzaSyAoJkXMU9V8t6Rn3Y_b_UkignLNAI305sk")

    def test_create_video(self):
        title = "Test Video"
        description = "This is a test video for CRUD operations."
        category_id = "27"  # Example category ID
        tags = ["test", "video", "CRUD"]
        result = self.client.create_video(title, description, category_id, tags)
        self.assertIsNotNone(result)  # Check if a response is returned
        self.assertIn("id", result)  # Check if the response contains a video ID

    def test_read_video(self):
        video_id = "Kz6IlDCyOUY"  # Replace with a valid video ID
        result = self.client.read_video(video_id)
        self.assertIn('items', result)

    def test_update_video(self):
        video_id = "Kz6IlDCyOUY"  # Replace with a valid video ID
        new_title = "Updated Test Video"
        new_description = "This is an updated description."
        result = self.client.update_video(video_id, title=new_title, description=new_description)
        self.assertIsNotNone(result)  # Check if the update was successful

    def test_delete_video(self):
        video_id = "Kz6IlDCyOUY"  # Replace with a valid video ID
        result = self.client.delete_video(video_id)
        self.assertIsNone(result)  # Check if the deletion was successful

if __name__ == '__main__':
    unittest.main()
