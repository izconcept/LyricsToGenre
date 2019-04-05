import lyricsgenius
import os
from pathlib import Path
import json
import threading
from dotenv import load_dotenv


# ----------------------- INITIALIZATION -----------------------

# Load .env variables into ENV
load_dotenv()

ROOT_DIR = Path(__file__).parents[2]
input_file = os.path.join(ROOT_DIR, 'data/songs.json')
output_file = os.path.join(ROOT_DIR, 'data/songsWithLyrics.json')

# Initialize RapGenius client
genius = lyricsgenius.Genius(os.getenv("GENIUS_TOKEN"))


# ----------------------- GENIUS SCRAPER THREAD CLASS -----------------------
class geniusScraperThread(threading.Thread):
    def __init__(self, data):
        super(geniusScraperThread, self).__init__()
        self.data = data

    def run(self):
        genius = lyricsgenius.Genius(os.getenv("GENIUS_TOKEN"))
        res = []
        for song in self.data:
            try:
                genius_data = genius.search_song(song["song"], song["artist"])

                if genius_data and genius_data.lyrics:
                    song["lyrics"] = genius_data.lyrics
                    res.append(song)
            except:
                print("Unexpected error:", sys.exc_info()[0])
        self.data = res


# ----------------------- ENTRYPOINT -----------------------
with open(input_file) as f:
    data = json.load(f)

SONGS_PER_THREAD = 250
thread_list = []

for i in range(0, len(data), SONGS_PER_THREAD):
    thread = geniusScraperThread(data[i: i + SONGS_PER_THREAD])
    thread_list.append(thread)
    thread.start()

for thread in thread_list:
    thread.join()

res = []
for thread in thread_list:
    res.extend(thread.data)

with open(output_file, 'w') as out:
    json.dump(res, out, indent=2)
