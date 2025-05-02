import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class SpotifyHandler:
    def __init__(self):
        """Initialize Spotify API client with OAuth authentication"""
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=os.getenv("CLIENT_ID"),
                client_secret=os.getenv("CLIENT_SECRET"),
                redirect_uri="http://127.0.0.1:8888/callback",
                scope="user-read-playback-state",
            )
        )

    def get_current_song(self):
        """
        Get the currently playing song and artist
        """
        playback = self.sp.current_playback()
        if playback and playback["is_playing"]:
            song = playback["item"]["name"]
            artist = playback["item"]["artists"][0]["name"]
            return song, artist
        return None, None

    def get_current_position(self):
        """
        Get the current playback position in milliseconds
        """
        current_playback = self.sp.current_playback()
        if current_playback and current_playback["is_playing"]:
            return current_playback["progress_ms"]
        return 0
