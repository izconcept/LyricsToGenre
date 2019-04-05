import lyricsgenius
import os
from pathlib import Path
import json
from dotenv import load_dotenv

# Load .env variables into ENV
load_dotenv()

ROOT_DIR = Path(__file__).parents[2]
input_file = os.path.join(ROOT_DIR, 'data/songs.json')
output_file = os.path.join(ROOT_DIR, 'data/songsandlyrics.json')

# Initialize RapGenius client
genius = lyricsgenius.Genius(os.getenv("GENIUS_TOKEN"))

# Get Lyric
# song = genius.search_song("estamos bien", "bad bunny")

with open(input_file) as f:
    data = json.load(f)
    for song in data:
        genius_data = genius.search_song(song["song"], song["artist"])

        if genius_data and genius_data.lyrics:
            song["lyrics"] = genius_data.lyrics

    with open(output_file, 'w') as out:
        json.dump(data, out)
