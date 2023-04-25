from googleapiclient.discovery import build
import json
import os


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        api_key = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel_info = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()

        self.__channel_id = channel_id
        self.title = channel_info['items'][0]["snippet"]['title']
        self.description = channel_info['items'][0]["snippet"]['description']
        self.url = f'https://www.youtube.com/channel/{channel_id}'
        self.subscriber_count = int(channel_info['items'][0]["statistics"]['subscriberCount'])
        self.video_count = int(channel_info['items'][0]["statistics"]['videoCount'])
        self.view_count = int(channel_info['items'][0]["statistics"]['viewCount'])

    def __repr__(self):
        return f'{self.title}("{self.url}")'

    def __add__(self, other):
        sum_subs = self.subscriber_count + other.subscriber_count
        return sum_subs

    def __sub__(self, other):
        subtracted_subs = self.subscriber_count - other.subscriber_count
        return subtracted_subs

    def __gt__(self, other):
        result = self.subscriber_count > other.subscriber_count
        return result

    def __ge__(self, other):
        result = self.subscriber_count >= other.subscriber_count
        return result

    def __lt__(self, other):
        result = self.subscriber_count < other.subscriber_count
        return result

    def __le__(self, other):
        result = self.subscriber_count <= other.subscriber_count
        return result

    def __eq__(self, other):
        result = self.subscriber_count == other.subscriber_count
        return result

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        api_key = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)

        return youtube

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        api_key = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)

        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(channel)

    def to_json(self, file_name) -> None:
        """Сохраняет в файл значения атрибутов экземпляра `Channel`"""
        with open(file_name, 'w') as json_file:
            channel_attributes = [
                                  {
                                   'channel_id': self.__channel_id,
                                   'title': self.title,
                                   'description': self.description,
                                   'url': self.url,
                                   'subscriber_count': self.subscriber_count,
                                   'video_count': self.video_count,
                                   'view_count': self.view_count
                                  }
                                 ]
            json.dump(channel_attributes, json_file)
            json_file.close()
