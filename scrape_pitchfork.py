import requests
import json
import csv
import scrape
import datetime
from bs4 import BeautifulSoup


def get_pitchfork_newreleases():
    results = list()
    PAGES_TO_SEARCH = 2

    # Search the pages and append to list of album dicts.
    for i in range(1, PAGES_TO_SEARCH + 1):
        search_url = "https://pitchfork.com/reviews/albums/?page=%d" % i
        page = requests.get(search_url, headers={'User-agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(page.content, 'html.parser')
        request_results = soup.find('body')

        # Scrape page for script that contains a "window.App" dict.
        request_results = request_results.find_all('script')
        for request_result in request_results:
            if(request_result.text[:10] == "window.App"):
                script_results = json.loads(request_result.text[11:-1])
                script_results = (script_results['context']['dispatcher']
                    ['stores']['ReviewsStore']['items'])
                break

        for result in script_results.values():
            # Check if result is a reissue. Can be -1 year for Dec -> Jan.
            album_year = (result['tombstone']['albums']
                [0]['album']['release_year'])
            current_year = datetime.datetime.today().year
            if current_year - album_year > 1 or result['tombstone']['bnr']:
                continue

            artist_str = result['artists'][0]['display_name'].strip()
            title_str = result['title']
            image_str = result['tombstone']['albums'][0]['album']
            image_str = image_str['photos']['tout']['sizes']['homepageLarge']
            rating_str = result['tombstone']['albums'][0]['rating']['rating']
            date_str = result['pubDate']

            genre_str = None
            if result['genres']:
                genre_str = result['genres'][0]['display_name']

            results.append({'artist': artist_str, 'title': title_str,
                'genre': genre_str, 'rating': float(rating_str),
                'image': image_str, 'date': date_str})

    return results


results = get_pitchfork_newreleases()
results = scrape.get_spotify_results(results)

# Create treblechef recommendation score
for result in results:
    if not('sp_popularity' in result):
        result['sp_popularity'] = 0
    result['score'] = (result['rating'] / 10) * 75 + \
        (result['sp_popularity'] / 100) * 25
    result['score'] = round(result['score'], 3)

# Sort by treblechef recommendation score.
results = sorted(results, key=lambda k: k['score'], reverse=True)

# Write results to csv and json files.
with open('results/results_pf.csv', mode='w') as csv_file:
    fieldnames = ['artist', 'title', 'genre', 'rating', 'date',
        'image', 'score', 'sp_artist', 'sp_genres', 'sp_popularity',
        'sp_followers', 'sp_id']
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    csv_writer.writeheader()
    csv_writer.writerows(results)

with open('results/results_pf.json', 'w') as json_file:
    json.dump(results, json_file, indent=4)
