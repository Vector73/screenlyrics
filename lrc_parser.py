import re
from syncedlyrics import search as synced_search


def parse_lrc(lyrics_text):
    """
    Parse LRC format lyrics into a list of timestamped lines
    """
    pattern = r"\[(\d+):(\d+\.\d+)\](.*)"
    parsed = []
    for line in lyrics_text.strip().splitlines():
        match = re.match(pattern, line)
        if match:
            minutes = int(match.group(1))
            seconds = float(match.group(2))
            total_seconds = minutes * 60 + seconds
            text = match.group(3).strip()
            parsed.append({"start": total_seconds, "text": text})
    return parsed


def get_lyrics(song, artist):
    """
    Search for synced lyrics for a song
    """
    lyrics = synced_search(f"'{song}' {artist}")
    if lyrics:
        return parse_lrc(lyrics)
    return []
