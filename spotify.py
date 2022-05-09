#!/usr/bin/env python3
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
load_dotenv()

class SpotifyClient():
    def __init__(self, scope):
        self.client = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

