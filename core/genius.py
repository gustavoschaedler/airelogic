import re

import bs4
from core.util import Util
from slugify import slugify
from bs4 import BeautifulSoup


class Genius:
    def __init__(self):
        self.search_url = 'https://genius.com/api/search/multi'
        self.artist_songs_url = 'https://genius.com/api/artists'
        self.util = Util()

    def get_artist_part(self, request_json: dict) -> list:
        artist_part = [
            art
            for art in request_json['response']['sections']
            if art['type'] == 'artist'
        ][0]['hits']

        return artist_part

    def get_artist_detail(self, artist: list, artist_name: str) -> list:
        artist_detail = [
            art['result']
            for art in artist
            if slugify(art['result']['name']) == slugify(artist_name)
        ]

        return artist_detail

    def get_artist(self, artist_name: str) -> dict:
        artist_result = {}
        artist, data = [], []

        url = f'{self.search_url}?q={artist_name}'
        request = self.util.request(url)

        if request.ok:
            artist = self.get_artist_part(request.json())

            if artist:
                data = self.get_artist_detail(artist, artist_name)

                if data:
                    artist_result = {
                        'id': data[0]['id'],
                        'name': data[0]['name'],
                        'url': data[0]['url'],
                        'api_path': data[0]['api_path']
                    }

        return artist_result

    def clean_lyrics(self, lyrics: str) -> str:
        # Remove [Verse], [Bridge], etc.
        lyrics = re.sub(r'(\[.*?\])*', '', lyrics)
        # Gaps between verses
        lyrics = re.sub('\n{2}', '\n', lyrics)

        return lyrics

    def count_words(self, lyrics) -> int:
        if lyrics is None:
            words = 0
        else:
            lyrics = self.clean_lyrics(
                lyrics.get_text()
            )
            words = len(lyrics.split())

        return words

    def scrape_lyrics(self, url: str):
        page = self.util.request(url)

        if page.text:
            html = BeautifulSoup(
                page.text.replace('<br/>', '\n'), 'html.parser'
            )
            div = html.find('div', class_=re.compile('^lyrics$|Lyrics__Root'))
        else:
            div = None

        return div

    def get_total_songs(self, artist_id: int) -> int:
        total_songs, next_page = 0, 1

        print('Getting total songs...')

        while next_page != None:
            url = f'{self.artist_songs_url}/{artist_id}/songs?per_page=50&page={next_page}'
            request = self.util.request(url)

            if request.ok:
                data = request.json()['response']
                next_page = data['next_page']
                total_songs += len(data['songs'])

        print(f'Found {total_songs} songs.')

        return total_songs

    def get_song_detail(self, song) -> dict:
        lyric_complete = (song['lyrics_state'] == 'complete')
        html_tag = self.scrape_lyrics(song['url']) if lyric_complete else None
        words = self.count_words(html_tag)

        data = {
            'song_name': song['title'],
            'lyric_url': song['url'],
            'lyric_complete': lyric_complete,
            'lyric_words': words
        }

        return data

    def get_songs(self, artist_id: int, artist_name: str) -> dict:
        counter, next_page = 0, 1
        songs, artist_songs = [], []

        total_songs = self.get_total_songs(artist_id)
        bar = self.util.custom_progress_bar(total_songs, 'scraped songs ')

        artist_songs = {
            'artist_id': artist_id,
            'artist_name': artist_name,
            'songs': []
        }

        while next_page != None:
            url = f'{self.artist_songs_url}/{artist_id}/songs?per_page=50&page={next_page}'
            request = self.util.request(url)

            if request.ok:
                data = request.json()['response']

                songs = data['songs']
                next_page = data['next_page']

                for song in songs:
                    counter += 1

                    if song['lyrics_state'] == 'complete':
                        artist_songs['songs'].append(
                            self.get_song_detail(song)
                        )

                    bar.update(counter)

        return artist_songs
