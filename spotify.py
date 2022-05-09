#!/usr/bin/env python3
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
load_dotenv()

SCOPES = ["playlist-modify-public", "playlist-modify-private"]

class SpotifyClient():
    def __init__(self, scope):
        self.client = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPES))
