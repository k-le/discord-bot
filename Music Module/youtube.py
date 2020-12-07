"""
Functions for Youtube API Client
"""

from dotenv import load_dotenv
import os
import json

from googleapiclient.discovery import build
import googleapiclient.errors
import google_auth_oauthlib.flow

from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

load_dotenv()
ytKEY = os.getenv('GOOGLE_KEY')  # load Google API Key

yt_name = 'youtube'    # bind input arguments for API client
yt_version = 'v3'
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
secrets_file = "googleSecrets.json"
playlistId = {PlaylistId of your desired Playlist here}


class YouTubeClient:

    def __init__(self, KEY: str):
        self.api_service_name = yt_name
        self.api_version = yt_version
        self.KEY = KEY
        self.youtube_client = self.get_youtube_client()

    def get_youtube_client(self):
        credential_path = os.path.join('./', 'credential_sample.json')
        store = Storage(credential_path)
        credentials = store.get()

        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(secrets_file, scopes)
            credentials = tools.run_flow(flow, store)

        youtube_client = build(self.api_service_name, self.api_version, credentials=credentials)

        return youtube_client

    def get_video_id(self, title: str):
        request = self.youtube_client.search().list(
            part='snippet',
            maxResults=25,
            q=title
        )
        response = request.execute()

        return response['items'][0]['id']

    def create_yt_playlist(self, title):
        request = self.youtube_client.playlists().insert(
            part='snippet',
            body={
                "snippet": {
                    "title": title,
                }
            }
        )
        response = request.execute()
        return response

    def add_vid_to_playlist(self, videoId: str):
        request = self.youtube_client.playlistItems().insert(
            part='snippet',
            body={
                'snippet': {
                    'playlistId': playlistId,
                    'resourceId': videoId
                }
            }
        )
        response = request.execute()

        return response
