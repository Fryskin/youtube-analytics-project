from googleapiclient.discovery import build
import os


class Video:
    def __init__(self, video_id):
        self.__api_key = os.getenv('API_KEY')
        self.__youtube = build('youtube', 'v3', developerKey=self.__api_key)

        video_response = self.__youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                      id=video_id).execute()

        self.video_id = video_id
        self.video_title = video_response['items'][0]['snippet']['title']
        self.video_url = f'https://www.youtube.com/watch?v={video_id}'
        self.view_count = video_response['items'][0]['statistics']['viewCount']
        self.likes_count = video_response['items'][0]['statistics']['likeCount']

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.video_id}')"

    def __str__(self):
        return self.video_title


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.video_id}', '{self.playlist_id}')"

    def __str__(self):
        return self.video_title
