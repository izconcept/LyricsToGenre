# LyricsToGenre
Determines the genre of a song based off its lyrics.


## Setup Virtual Environment (Optional)

* Have pip installed for python3 (pip3)
* `python3 -m pip install --user virtualenv`
* `python3 -m virtualenv venv`

### Activate Virtual Environment
`source venv/bin/activate`

### Install Packages
`pip3 install -r requirements.txt`

### Deactivate Virtual Environment
`deactivate`

## Setup Environment Variables

*TBD*

## Run Scrapers

### Run Billboard Scraper

Navigate to scrapy directory: 
`cd scraper/billboard_scraper`

Run:
`scrapy crawl billboard`

Run and Save:
`scrapy crawl billboard -o ../../data/songs.json`

### Run Lyrics (Genius) Scraper

`python scraper/lyrics/genius_scraper.py`
