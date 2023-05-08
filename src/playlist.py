import isodate
from googleapiclient.discovery import build
import os
import datetime


class PlayList:

    def __init__(self, playlist_id: str):
        self.__api_key = os.getenv('API_KEY')
        self.__youtube = build('youtube', 'v3', developerKey=self.__api_key)

        title_info = self.__youtube.playlists().list(id=playlist_id, part='snippet').execute()

        self._playlist_id = playlist_id
        self.title = title_info["items"][0]["snippet"]["title"]
        self.url = f"https://www.youtube.com/playlist?list={playlist_id}"

    def total_duration(self):

        playlist_videos = self.__youtube.playlistItems().list(playlistId=self._playlist_id, part='contentDetails',
                                                              maxResults=50,
                                                              ).execute()

        video_ids = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = self.__youtube.videos().list(part='contentDetails,statistics', id=','.join(video_ids)
                                                      ).execute()

        total_video_duration = datetime.timedelta(hours=0, minutes=0, seconds=0)

        for video in video_response['items']:

            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)

            duration_split = str(duration).split(':')
            duration = datetime.timedelta(hours=int(duration_split[0]), minutes=int(duration_split[1]),
                                          seconds=int(duration_split[2]))
            total_video_duration += duration

        return total_video_duration

    def show_best_video(self):

        playlist_videos = self.__youtube.playlistItems().list(playlistId=self._playlist_id, part='contentDetails',
                                                              maxResults=50,
                                                              ).execute()

        video_ids = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = self.__youtube.videos().list(part='contentDetails,statistics', id=','.join(video_ids)
                                                      ).execute()

        best_video_like_count = 0
        best_video_url = ''
        for video in video_response['items']:

            like_count = int(video['statistics']['likeCount'])

            if like_count > best_video_like_count:
                best_video_like_count = like_count
                best_video_url = f"https://youtu.be/{video['id']}"

        return best_video_url
