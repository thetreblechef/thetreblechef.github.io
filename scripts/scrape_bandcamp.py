import requests
import json
import csv
import scrape
from datetime import datetime


def get_bandcamp_releases(tag_str):
    url = 'https://bandcamp.com/api/hub/2/dig_deeper'
    PAGES_TO_SEARCH = 10
    GENRES_TO_IGNORE = ['metal', 'podcasts', 'classical', 'ambient']

    results = list()
    for i in range(1, PAGES_TO_SEARCH + 1):
        json_obj = {"filters": {"format": "all", "location": 0,
            "sort": "pop", "tags": [tag_str]}, "page": i}
        x = requests.post(url, json=json_obj)
        request_results = json.loads(x.text)

        for result in request_results['items']:
            # Skip albums that have genre within the ignore list.
            genre_str = result['genre']
            if genre_str in GENRES_TO_IGNORE:
                continue

            artist_str = result['artist']
            title_str = result['title']
            image_str = 'https://f4.bcbits.com/img/a%s_2.jpg' \
                % result['art_id']
            url_str = result['tralbum_url']

            results.append({'artist': artist_str, 'title': title_str,
                'genre': genre_str, 'image': image_str, 'url': url_str})

    return results


def get_bandcamp_scores(results):
    for result in results:
        if not('sp_popularity' in result):
            result['sp_popularity'] = 0
        date_obj = datetime.strptime(result['sp_date'], "%Y-%m-%dT00:00.000Z")
        time_score = 60 - (datetime.now() - date_obj).days
        result['score'] = result['sp_popularity'] / 100 * 75 + \
            time_score / 60 * 25
        result['score'] = round(result['score'], 3)

    # Sort by treblechef recommendation score.
    results = sorted(results, key=lambda k: k['score'], reverse=True)
    return results


for tag_str in ['toronto', 'montreal', 'vancouver']:
    results = get_bandcamp_releases(tag_str)
    results = scrape.get_spotify_albums(results)
    results = scrape.get_spotify_results(results)
    results = get_bandcamp_scores(results)

    # Write results to csv and json files.
    with open('results/%s.csv' % tag_str, mode='w') as csv_file:
        fieldnames = ['artist', 'title', 'genre', 'url',
            'image', 'score', 'sp_artist', 'sp_popularity',
            'sp_date', 'sp_img', 'sp_album_id', 'sp_artist_id']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        csv_writer.writeheader()
        csv_writer.writerows(results)

    with open('results/%s.json' % tag_str, 'w') as json_file:
        json.dump(results, json_file, indent=4)
