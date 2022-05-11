#!/usr/bin/env python3
from typing import Any
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
load_dotenv()

SCOPES = ["playlist-modify-public", "playlist-modify-private", "playlist-read-private"]

class SpotifyClient():
    def __init__(self):
        self.client: Any = None
        self.auth = SpotifyOAuth(scope=SCOPES, open_browser=False)
        self.authorize_url = self.auth.get_authorize_url()
        self.auth_object = None

    def authorizeClient(self, response_url):
        response_code = self.auth.parse_response_code(response_url)
        self.auth_object = self.auth.get_access_token(response_code)
        self.access_token = self.auth_object["access_token"]
        self.client = spotipy.Spotify(auth=self.access_token)

    def searchForPlaylist(self, name, limit):
        playlists = self.client.current_user_playlists(limit=limit)
        offset = 0
        while True:
            for playlist in playlists["items"]:
                if name in playlist["name"]:
                    return playlist
            offset += limit
            playlists = self.client.current_user_playlists(offset=offset, limit=limit)

    def getOrCreatePlaylist(self):
        if (playlist := self.searchForPlaylist("Playlistify - Spotify Playlist", 50)):
            return playlist
        else:
            playlist = self.client.user_playlist_create(user=self.client.me()["id"], name="Playlistify - Spotify Playlist", public=False)
            return playlist



if __name__ == "__main__":
    client = SpotifyClient()
    print(f"Authorize URL: {client.authorize_url}")
    response_url = input("Response URL: ")
    client.authorizeClient(response_url)
    playlist = client.getOrCreatePlaylist()
