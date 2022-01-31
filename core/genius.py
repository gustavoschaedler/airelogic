import re
import progressbar
from core.util import Util
from slugify import slugify
from bs4 import BeautifulSoup
from progressbar import ProgressBar


class Genius:
    def __init__(self):
        self.search_url = 'https://genius.com/api/search/multi'
        self.artist_songs_url = 'https://genius.com/api/artists'
        self.util = Util()

    def get_artist(self, artist_name: str) -> dict:
        artist_result = {}
        artist, data = [], []

        url = f'{self.search_url}?q={artist_name}'
        request = self.util._request(url)

        if request.status_code in [200, 204]:
            # Filter artist part
            artist = [
                art
                for art in request.json()['response']['sections']
                if art['type'] == 'artist'
            ][0]['hits']

            # Filter artist list and slug name compare
            if artist:
                # Match artist data
                data = [
                    art['result']
                    for art in artist
                    if slugify(art['result']['name']) == slugify(artist_name)
                ]

                if data:
                    artist_result = {
                        'id': data[0]['id'],
                        'name': data[0]['name'],
                        'url': data[0]['url'],
                        'api_path': data[0]['api_path']
                    }

        return artist_result

    def scrape_lyrics(self, url: str) -> int:
        page = self.util._request(url)
        html = BeautifulSoup(page.text.replace('<br/>', '\n'), 'html.parser')
        # Filter by class of the div
        div = html.find('div', class_=re.compile('^lyrics$|Lyrics__Root'))

        if div is None:
            text, words = None, 0
        else:
            lyrics = div.get_text()
            # Remove [Verse], [Bridge], etc.
            lyrics = re.sub(r'(\[.*?\])*', '', lyrics)
            # Gaps between verses
            lyrics = re.sub('\n{2}', '\n', lyrics)

            text = lyrics.strip("\n")
            words = len(lyrics.split())

        return words

    def get_total_songs(self, artist_id: int) -> dict:
        total_songs, next_page = 0, 1

        print('Getting total songs...')

        while next_page != None:
            url = f'{self.artist_songs_url}/{artist_id}/songs?per_page=50&page={next_page}'
            request = self.util._request(url)

            if request.status_code in [200, 204]:
                data = request.json()['response']
                next_page = data['next_page']

                total_songs += len(data['songs'])

        print(f'Found {total_songs} songs.')

        return total_songs

    def get_songs(self, artist_id: int, artist_name: str) -> dict:
        counter, next_page = 0, 1
        songs, artist_songs = [], []

        total_songs = self.get_total_songs(artist_id)

        widgets = [
            progressbar.Percentage(), ' (', progressbar.Counter(
            ), ' of ', str(total_songs), ') scraped songs ',
            progressbar.Bar(),
            ' [', progressbar.Timer(), '] ',
            ' (', progressbar.ETA(), ') ',
        ]

        bar = ProgressBar(
            max_value=total_songs,
            widgets=widgets,
            redirect_stdout=True
        )

        artist_songs = {
            'artist_id': artist_id,
            'artist_name': artist_name,
            'songs': []
        }

        while next_page != None:
            url = f'{self.artist_songs_url}/{artist_id}/songs?per_page=50&page={next_page}'
            request = self.util._request(url)

            if request.status_code in [200, 204]:
                data = request.json()['response']

                songs = data['songs']
                next_page = data['next_page']

                for _, song in enumerate(songs):
                    counter += 1
                    lyric_url = song['url']
                    lyric_name = song['title']
                    lyric_complete = (song['lyrics_state'] == 'complete')
                    lyric_primary_artist_id = song['primary_artist']['id'] == artist_id

                    # Filter if [primary artist id] == [artist_id]
                    if lyric_primary_artist_id:
                        words = self.scrape_lyrics(
                            lyric_url) if lyric_complete else 0

                        song_detail = {
                            'song_name': lyric_name,
                            'lyric_url': lyric_url,
                            'lyric_complete': lyric_complete,
                            'lyric_words': words
                        }
                        artist_songs['songs'].append(song_detail)

                    bar.update(counter)

        return artist_songs
