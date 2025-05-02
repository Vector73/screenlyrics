# Spotify Lyrics Visualizer

A floating window that displays synced lyrics for your currently playing Spotify track with animations and visual effects.

## Requirements

- Python 3.6+
- Spotify Developer credentials

## Setup

1. Clone this repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Create a Spotify Developer app at https://developer.spotify.com/dashboard/
4. Add `http://127.0.0.1:8888/callback` as a redirect URI in your Spotify app settings
5. Copy `.env.example` to `.env` and add your Spotify credentials:
   ```
   CLIENT_ID=your_spotify_client_id_here
   CLIENT_SECRET=your_spotify_client_secret_here
   ```

## Usage

1. Start playing a song on Spotify
2. Run the application:
   ```
   python main.py
   ```
3. The lyrics should appear in a floating window, synchronized with the music.

## Troubleshooting

- If you're not seeing lyrics, check that your song has available synced lyrics
- Ensure your Spotify account is properly authenticated
- Check your internet connection
- Verify that your Spotify Developer credentials are correct in the `.env` file
