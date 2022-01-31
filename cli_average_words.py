#!/usr/bin/env python

import fire


def avg(artist_name: str) -> str:
    """Return the average (mean) number of words in an artist's discography.

    Args:
        artist_name (str): Artist name

    Returns:
        str: Average number of words in an artist's discography.
    """

    from core.util import Util
    from core.genius import Genius

    songs_avg = 0
    util = Util()
    genius = Genius()

    util.banner('Aire Logic\nCode Challenge')

    artist = genius.get_artist(artist_name)

    if artist:
        songs_list = genius.get_songs(artist['id'], artist['name'])
        songs_avg = util.calc_avg_words_from_songs_list(songs_list['songs'])
        data = f'AVG Words: {songs_avg}'
    else:
        data = f'Artist: "{artist_name}" not found on Genius.com database.'

    print(f'\n\n{data}')


def _main():
    fire.Fire()


if __name__ == '__main__':
    _main()
