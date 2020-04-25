import requests
import json
import csv
import scrape
from datetime import datetime
# from bs4 import BeautifulSoup


def get_bandcamp_releases():
    url = 'https://bandcamp.com/api/hub/2/dig_deeper'
    PAGES_TO_SEARCH = 10
    GENRES_TO_IGNORE = ['metal', 'podcasts', 'classical']

    results = list()
    for i in range(1, PAGES_TO_SEARCH + 1):
        json_obj = {"filters": {"format": "all", "location": 0,
            "sort": "pop", "tags": ["toronto"]}, "page": i}
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

    # Code required to find the date of each release. Long runtime.
    # Searching each individual album via spotipy much faster.
    # for result in results:
    #    print(result['url'])
    #    page = requests.get(result['url'])

        # Searching string faster than scraping entire webpage.
        # Search for releases or released. Time taken HPC ~ 0.015s
    #    request_str = repr(str(page.content))
    #    idx1 = request_str.find(' release') + 10
    #    idx2 = request_str[idx1:].find('\\n') + idx1 - 1
    #    date_str = request_str[idx1:idx2]
    #    month_str = datetime.strptime(date_str[3:-5], '%B').month
    #    date_str = "%s-%02d-%s" % (date_str[-4:], month_str, date_str[0:2])
    #    print(date_str)

    return results


results = get_bandcamp_releases()
results = scrape.get_spotify_albums(results)
results = scrape.get_spotify_results(results)

for result in results:
    if not('sp_popularity' in result):
        result['sp_popularity'] = 0
    date_obj = datetime.strptime(result['sp_date'], "%Y-%m-%dT00:00.000Z")
    time_score = 90 - (datetime.now() - date_obj).days
    result['score'] = result['sp_popularity'] / 100 * 75 + time_score / 90 * 25
    result['score'] = round(result['score'], 3)

# Sort by treblechef recommendation score.
results = sorted(results, key=lambda k: k['score'], reverse=True)

# Write results to csv and json files.
with open('results/results_bc.csv', mode='w') as csv_file:
    fieldnames = ['artist', 'title', 'genre', 'url',
        'image', 'score', 'sp_artist', 'sp_popularity',
        'sp_followers', 'sp_date', 'sp_img', 'sp_album_id', 'sp_artist_id']
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    csv_writer.writeheader()
    csv_writer.writerows(results)

with open('results/results_bc.json', 'w') as json_file:
    json.dump(results, json_file, indent=4)
