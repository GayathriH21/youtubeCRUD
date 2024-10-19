import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

class YouTubeClient:
    def __init__(self):
        self.scopes = [
            "https://www.googleapis.com/auth/youtube.upload",       # For uploading videos
            "https://www.googleapis.com/auth/youtube.readonly",     # For reading video details
            "https://www.googleapis.com/auth/youtube.force-ssl"     # For full access to YouTube
        ]
        self.youtube = self.authenticate()

    def authenticate(self):
        credentials = None

        # Load credentials from the token.pickle file if it exists
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                credentials = pickle.load(token)

        # If no valid credentials, start OAuth flow
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.scopes)
                credentials = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(credentials, token)

        # Build the YouTube service
        return build('youtube', 'v3', credentials=credentials)

    def create_video(self, title, description, category_id, tags, video_file_path):
        try:
            # Upload the video file
            media = MediaFileUpload(video_file_path, chunksize=-1, resumable=True)

            # Insert video metadata and upload the video
            request = self.youtube.videos().insert(
                part="snippet,status",
                body={
                    "snippet": {
                        "title": title,
                        "description": description,
                        "tags": tags,
                        "categoryId": category_id
                    },
                    "status": {
                        "privacyStatus": "public"  # Change privacy setting as needed
                    }
                },
                media_body=media
            )
            response = request.execute()
            return response
        except HttpError as e:
            print(f"An error occurred while uploading the video: {e}")
            return None

    def read_video(self, video_id):
        try:
            request = self.youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=video_id
            )
            response = request.execute()
            return response
        except HttpError as e:
            print(f"An error occurred while reading video: {e}")
            return None

    def update_video(self, video_id, title=None, description=None):
        try:
            video_details = self.read_video(video_id)
            if not video_details or 'items' not in video_details or not video_details['items']:
                print("No video found or insufficient permissions to read video details.")
                return None

            snippet = video_details['items'][0]['snippet']
            if title:
                snippet['title'] = title
            if description:
                snippet['description'] = description

            request = self.youtube.videos().update(
                part="snippet",
                body={
                    "id": video_id,
                    "snippet": snippet
                }
            )
            response = request.execute()
            return response
        except HttpError as e:
            print(f"An error occurred while updating video: {e}")
            return None

    def delete_video(self, video_id):
        try:
            request = self.youtube.videos().delete(id=video_id)
            response = request.execute()
            return response
        except HttpError as e:
            print(f"An error occurred while deleting video: {e}")
            return None


def main():
    client = YouTubeClient()

    while True:
        print("\nChoose an operation:")
        print("1. Create Video")
        print("2. Read Video")
        print("3. Update Video")
        print("4. Delete Video")
        print("5. Exit")

        choice = input("Enter the number corresponding to the operation: ")

        if choice == '1':
            title = input("Enter video title: ")
            description = input("Enter video description: ")
            category_id = input("Enter category ID: ")
            tags_input = input("Enter tags (comma-separated): ")
            tags = tags_input.split(',')
            video_file_path = input("Enter the path to the video file: ")  # This is the file you want to upload
            result = client.create_video(title, description, category_id, tags, video_file_path)
            print(f"Created video with response: {result}")

        elif choice == '2':
            video_id = input("Enter video ID to read: ")
            result = client.read_video(video_id)
            print(f"Video details: {result}")

        elif choice == '3':
            video_id = input("Enter video ID to update: ")
            title = input("Enter new title (or leave blank to skip): ")
            description = input("Enter new description (or leave blank to skip): ")
            result = client.update_video(video_id, title if title else None, description if description else None)
            print(f"Updated video with response: {result}")

        elif choice == '4':
            video_id = input("Enter video ID to delete: ")
            result = client.delete_video(video_id)
            print(f"Deleted video with response: {result}")

        elif choice == '5':
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    main()
