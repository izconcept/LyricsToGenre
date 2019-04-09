import os
import sys
import random
import json
from pathlib import Path


ROOT_DIR = Path(__file__).parents[1]
filename = os.path.join(ROOT_DIR, 'data/songs.json')

with open(filename) as f:
    songs = json.load(f)

song_map = {
    '1': 'country',
    '2': 'pop',
    '3': 'hiphop',
    '4': 'rock',
    '5': 'latin',
    '6': 'christian',
    '7': 'electronic'
    }

count = 0
correct_count = 0
while True:
    song = random.choice(songs)
    if 'lyrics' not in song: continue
    print(song['lyrics'])
    print('\nWhat genre is this song: 1. country, 2. pop, 3. hiphop, 4. rock, 5. latin, 6. christian, 7. electronic \nType any other value to exit')
    value = input("Enter another number: ")
    if value not in song_map:
        break
    if song_map[value] == song['genre']:
        correct_count += 1
    count += 1
    print('Correct answer: ', song['genre'])

print('Accuracy: ', correct_count / count)
