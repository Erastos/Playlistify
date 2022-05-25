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
        for _ in range(5):
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

    def getAllTrackIds(self, playlist_id):
        tracks = self.client.playlist_tracks(playlist_id)
        track_ids = []

        while tracks["next"] is not None:
            track_ids.extend([track["track"]["id"] for track in tracks["items"]])
            tracks = self.client.next(tracks)
        track_ids.extend([track["track"]["id"] for track in tracks["items"]])

        return track_ids

    def addDifferentSongs(self, playlist_id, track_ids):
        tracks = self.getAllTrackIds(playlist_id)
        tracks_add = list(set(track_ids).difference(tracks))
        self.client.playlist_add_items(playlist_id, tracks_add)
        return tracks_add




if __name__ == "__main__":
    client = SpotifyClient()
    print(f"Authorize URL: {client.authorize_url}")
    response_url = input("Response URL: ")
    client.authorizeClient(response_url)
    playlist = client.getOrCreatePlaylist()
    tracks = client.addDifferentSongs(playlist["id"], ["2W29TNaSCiolWbPfQNgNOW"])
