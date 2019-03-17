import lyricsgenius
import os

from dotenv import load_dotenv

# Load .env variables into ENV
load_dotenv()

# Initialize RapGenius client
genius = lyricsgenius.Genius(os.getenv("GENIUS_TOKEN"))

# Get Lyric
song = genius.search_song("estamos bien", "bad bunny")
print(song.lyrics)
