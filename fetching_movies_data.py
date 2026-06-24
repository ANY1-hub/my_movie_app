import os
import requests
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / "config" / ".env")

API_KEY = os.getenv('OMDB_API_KEY')
if not API_KEY: API_KEY = ''


# ==============================================================================
# fetching data
# ==============================================================================

# noinspection GrazieInspection
def fetch_data(title: str):
    '''
    fetches movie data form an api by movie title
    :param title: title of movie to fetch data about
    :return: a JSON of movie data:
    {
        "Title": "Titanic",
        "Year": "1997",
        "imdbRating": "8.0",
        "Poster": "https://m.media/..."
    },
    '''
    REQUEST_URL = 'http://www.omdbapi.com/?'
    if not API_KEY:
        print("ERROR: No API key provided.")
        print("Set OMDB_API_KEY env var or paste it in the script.")
        sys.exit(1)
    parameters = {
        'apikey': API_KEY,
        't': title
    }
    try:
        resp = requests.get(REQUEST_URL, params=parameters)
        # raise for 4xx/5xx
        resp.raise_for_status()
        resp = resp.json()
        if resp["Response"] == 'False':
            return None
        transformed_movie_data = {'title': resp['Title'],
                                  'year': resp['Year'],
                                  'rating': resp['imdbRating'],
                                  'poster': resp['Poster']
                                  }
        return transformed_movie_data

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print("Response body:", e.response.text)
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        sys.exit(1)
