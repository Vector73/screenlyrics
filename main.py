from spotify_handler import SpotifyHandler
from lrc_parser import get_lyrics
from ui_components import LyricsWindow


def main():
    """Initialize and start the application"""
    spotify = SpotifyHandler()
    window = LyricsWindow(spotify, get_lyrics)

    print("Getting Lyrics...")
    window.start()


if __name__ == "__main__":
    main()
