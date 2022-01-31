import requests
import pyfiglet
from time import sleep
from pandas import DataFrame
from requests.exceptions import HTTPError, Timeout


class Util:
    def banner(self, text: str) -> None:
        print(pyfiglet.figlet_format(text))

    def dict_to_dataframe(self, data: dict) -> DataFrame:
        import pandas as pd
        return pd.DataFrame.from_dict(data)

    def calc_avg_words_from_songs_list(self, songs_list: dict) -> float:
        df = self.dict_to_dataframe(songs_list)
        return round(df['lyric_words'].mean(), 2)

    def _request(self, url: str):
        tries = 1
        response = None
        max_retries = 5
        sleep_retrie = 3

        while (response is None) and (tries <= max_retries):
            try:
                response = requests.get(url, timeout=5)
                response.raise_for_status()
            except Timeout as e:
                error = f'Request timed out:\n{e}'
                if tries > max_retries:
                    raise Timeout(error)
            except HTTPError as e:
                if (response.status_code < 500) or (tries > max_retries):
                    raise HTTPError(response.status_code, e)
            except Exception as e:
                print(
                    f'No internet connection: sleep {sleep_retrie} seconds... retrie ({tries} of {max_retries})')
                sleep(sleep_retrie)

            tries += 1
            sleep(0.2)

        if response:
            if response.status_code in [200, 204]:
                return response
            else:
                raise AssertionError(
                    f'Response status code was neither 200, nor 204. It was {response.status_code} - Url: {url}')
        else:
            raise AssertionError('No internet connection, try again later.')
