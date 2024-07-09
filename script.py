import os
import pandas as pd
from googleapiclient.discovery import build

from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('API_KEY')


youtube = build('youtube', 'v3', developerKey=API_KEY)


def search_videos(query, max_results=100):
    response = youtube.search().list(
        q=query,
        part='snippet',
        maxResults=max_results,
        type='video'
    ).execute()

    videos = []
    for item in response['items']:
        video_id = item['id']['videoId']
        video_details = youtube.videos().list(
            part='snippet,statistics',
            id=video_id
        ).execute()
        video = video_details['items'][0]
        videos.append({
            'Title': video['snippet']['title'],
            'Description': video['snippet']['description'],
            'Author': video['snippet']['channelTitle'],
            'Views': video['statistics'].get('viewCount', 0),
            'URL': f"https://www.youtube.com/watch?v={video_id}"
        })
    return videos


queries = ['Children Education', 'Education Technology']


all_videos = []
for query in queries:
    videos = search_videos(query)
    all_videos.extend(videos)


df = pd.DataFrame(all_videos)
df.to_csv('education_videos.csv', index=False)


