import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Create a spotipy object to query spotify. Requires exporting
# SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET as environment variables.
# https://spotipy.readthedocs.io/en/2.11.2/
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


# Given a list of album dicts, search details about the primary artist.
def get_spotify_results(results):
    for result in results:
        # Spotify results.
        sp_results = sp.search(result['artist'], type='artist', limit=5)
        sp_results = sp_results['artists']['items']
        if not(sp_results):
            continue

        # Ensure the Spotify result matches artist name.
        sp_result = None
        for s in sp_results:
            if s['name'].lower() == result['artist'].lower():
                sp_result = s
                break
        if not(sp_result):
            continue

        result['sp_artist'] = sp_result['name']
        result['sp_genres'] = sp_result['genres']
        result['sp_popularity'] = sp_result['popularity']
        result['sp_followers'] = sp_result['followers']['total']
        result['sp_id'] = sp_result['id']
    return results
