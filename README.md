# Aire Logic Tech Test

Produce a program which, when given the name  of an artist, will produce the average (mean) number of words in their songs.

<table border="1">
    <thead>
        <tr>
            <th><b>Artist</b></th>
            <th><b>Album</b></th>
            <th><b>Songs</b></th>
            <th><b>Words</b></th>
            <th colspan="2"><b>Avg</b></th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan="10">Eminem</td>
            <td rowspan="5">Album 03</td>
            <td>Song 01</td>
            <td>230</td>
            <td rowspan="5">250</td>
            <td rowspan="10"><b>218</b></td>
        </tr>
        <tr>
            <td>Song 02</td>
            <td>120</td>
        </tr>
        <tr>
            <td>Song 03</td>
            <td>321</td>
        </tr>
        <tr>
            <td>Song 04</td>
            <td>451</td>
        </tr>
        <tr>
            <td>Song 05</td>
            <td>128</td>
        </tr>
        <tr>
            <td rowspan="3">Album 02</td>
            <td>Song 01</td>
            <td>100</td>
            <td rowspan="3">186<br></td>
        </tr>
        <tr>
            <td>Song 02</td>
            <td>143</td>
        </tr>
        <tr>
            <td>Song 03</td>
            <td>315</td>
        </tr>
        <tr>
            <td>...</td>
            <td>...</td>
            <td>...</td>
            <td>...</td>
        </tr>
        <tr>
            <td>Album N</td>
            <td>Song N</td>
            <td>xxx</td>
            <td>yyy</td>
        </tr>
    </tbody>
</table>

## Data flow

```text
1) artist_name
2) get_artist(artist_name)
3) get_total_songs(artist_id)
4) get_songs(artist_id, artist_name)
5) scrape_lyrics(url)
6) calc_avg_words_from_songs_list(songs_list)
```

## 1. Installation

### 1.1 To repo clone

```bash
git clone https://github.com/gustavoschaedler/airelogic.git
```

### 1.2 To create a virtualenv
```bash
python3 -m venv .venv
```

### 1.3 To activate the virtualenv
```bash
source .venv/bin/activate
```

### 1.4 To install all requirements
```bash
pip3 install -r requirements.txt
```

#### Requirements list
- **fire** - Used to manage the cli.
- **pandas** - Used to consolidate data and average words.
- **requests** - Used to make requests to API endpoints.
- **pyfiglet** - Used to create the initial banner with the text "Aire Logic Code Challenge".
- **progressbar2** - Used to control the progress bar.
- **python-slugify** - Used to turn artist name into slug text.
- **beautifulsoup4** - Used to scrape the lyrics.

## 2. Basic Usage

### 2.1 Help commands

```bash
python cli_average_words.py
python cli_average_words.py --help
```

Result:
```text
NAME
    cli_average_words.py

SYNOPSIS
    cli_average_words.py GROUP | COMMAND

GROUPS
    GROUP is one of the following:

     fire
       The Python Fire module.

COMMANDS
    COMMAND is one of the following:

     avg
       Return the average (mean) number of words in an artist's discography.
```

```bash
python cli_average_words.py avg --help
```

Result:
```text
NAME
    cli_average_words.py avg - Return the average (mean) number of words in an artist's discography.

SYNOPSIS
    cli_average_words.py avg ARTIST_NAME

DESCRIPTION
    Return the average (mean) number of words in an artist's discography.

POSITIONAL ARGUMENTS
    ARTIST_NAME
        Type: str
        Artist name

NOTES
    You can also use flags syntax for POSITIONAL ARGUMENTS
```

### 2.2 To calculate the average
```bash
python cli_average_words.py avg U2
```

If the artist name has more than one word, you must provide the name as a string. eg. "Eric Clapton"

```bash
python cli_average_words.py avg "Eric Clapton"
```
Result:
```text
    _    _            _                _      
   / \  (_)_ __ ___  | |    ___   __ _(_) ___ 
  / _ \ | | '__/ _ \ | |   / _ \ / _` | |/ __|
 / ___ \| | | |  __/ | |__| (_) | (_| | | (__ 
/_/   \_\_|_|  \___| |_____\___/ \__, |_|\___|
                                 |___/        
  ____          _         ____ _           _ _                       
 / ___|___   __| | ___   / ___| |__   __ _| | | ___ _ __   __ _  ___ 
| |   / _ \ / _` |/ _ \ | |   | '_ \ / _` | | |/ _ \ '_ \ / _` |/ _ \
| |__| (_) | (_| |  __/ | |___| | | | (_| | | |  __/ | | | (_| |  __/
 \____\___/ \__,_|\___|  \____|_| |_|\__,_|_|_|\___|_| |_|\__, |\___|
                                                          |___/      

Getting total songs...
Found 1009 songs.
100% (1009 of 1009) scraped songs |##################| [Elapsed Time: 0:09:20]  (ETA:  00:00:00) 

AVG Words: 151.83
```




