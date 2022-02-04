from urllib import response
import pyfiglet
import progressbar
from requests import Session
from urllib3.util import Retry
from progressbar import ProgressBar
from requests.adapters import HTTPAdapter


class APIGeniusRequestError(ConnectionError):
    pass


class Util:
    def banner(self, text: str) -> None:
        print(pyfiglet.figlet_format(text))

    def calc_avg_words_from_songs_list(self, field_name_lyric_words: str, songs_list: dict) -> float:
        avg, count_songs, total_words = 0, 0, 0

        for song in songs_list:
            count_songs += 1
            total_words += song[field_name_lyric_words]

        if count_songs >= 0:
            avg = round(total_words/count_songs, 2)

        return avg

    def custom_progress_bar(self, total, text) -> ProgressBar:
        widgets = [
            progressbar.Percentage(), ' (', progressbar.Counter(
            ), ' of ', str(total), ') ', text,
            progressbar.Bar(),
            ' [', progressbar.Timer(), '] ',
            ' (', progressbar.ETA(), ') ',
        ]

        bar = ProgressBar(
            max_value=total,
            widgets=widgets,
            redirect_stdout=True
        )

        return bar

    def retry_session(self, total: int = 5, backoff_factor: float = 0.5, method_whitelist: set = ['GET']) -> Session:
        strategy = Retry(
            total=total,
            backoff_factor=backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=frozenset(method_whitelist)
        )

        adapter = HTTPAdapter(max_retries=strategy)

        session = Session()
        session.mount("https://", adapter)
        session.mount("http://", adapter)

        return session

    def request(self, url: str, timeout: int = 2):
        request_session = self.retry_session()

        try:
            response = request_session.get(url, timeout=timeout)
        except Exception as err:
            print(f'No internet connection error: {err.__class__.__name__}')
            raise APIGeniusRequestError
        else:
            return response
