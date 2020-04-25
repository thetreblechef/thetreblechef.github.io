import requests
import json
import csv
import scrape
from bs4 import BeautifulSoup


def get_allmusic_newreleases():
    search_url = "https://www.allmusic.com/newreleases"
    GENRE_IGNORE_LIST = ['Country', 'Classical']
    PAGES_TO_SEARCH = 2

    # Get the pages to search through.
    page = requests.get(search_url, headers={'User-agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(page.content, 'html.parser')
    request_results = soup.find('select', class_='week-filter')
    request_results = request_results.find_all('option')
    search_id_list = list()
    for result in request_results:
        if result.get('value')[0] == '2':
            search_id_list.append(result.get('value'))

    # Search the pages and append to list of album dicts.
    results = list()
    for search_id in search_id_list[:PAGES_TO_SEARCH]:
        search_url = "https://www.allmusic.com/newreleases/%s" % search_id
        page = requests.get(search_url, headers={'User-agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(page.content, 'html.parser')

        request_results = soup.find_all('div', class_='new-release')

        for idx, request_result in enumerate(request_results):
            img = request_result.find('div', class_='image-container')
            meta = request_result.find('div', class_='meta-container')
            artist = meta.find('div', class_='artist')
            title = meta.find('div', class_='title')
            genre = meta.find('div', class_='genres')

            artist_str = artist.get_text().replace('\n', '')[:-1]
            title_str = title.get_text().replace('\n', '')[:-1]
            genre_str = genre.get_text().replace('\n', '')[:-1]
            image_str = img.find('img', class_='lazy')['data-original']
            stars = len(meta.find_all('img', class_='blue star')) + \
                0.5 * len(meta.find_all('img', class_='blue half'))

            # choice_flag = False
            # if "Editors' Choice" in img.get_text():
            #     choice_flag = True

            # Skip albums that meet certain criteria.
            if any(gen in genre_str for gen in GENRE_IGNORE_LIST):
                continue
            if "Various Artists" in artist_str:
                continue

            # Select primary artist for albums with collaborators.
            if ' / ' in artist_str:
                artist_str = artist_str[:artist_str.find(' / ')]

            # Find the date that the review was submitted.
            tmp = search_id
            date_str = "%s-%s-%sT00:00.000Z" % (tmp[:4], tmp[4:6], tmp[6:8])

            results.append({'artist': artist_str, 'title': title_str,
                'genre': genre_str, 'rating': stars, 'image': image_str,
                'date': date_str})

    return results


results = get_allmusic_newreleases()
results = scrape.get_spotify_results(results)

# Create treblechef recommendation score.
for result in results:
    if not('sp_popularity' in result):
        result['sp_popularity'] = 0
    result['score'] = (result['rating'] / 5) * 75 + \
        (result['sp_popularity'] / 100) * 25
    result['score'] = round(result['score'], 3)

# Sort by treblechef recommendation score.
results = sorted(results, key=lambda k: k['score'], reverse=True)

# Write results to csv and json files.
with open('results/results_am.csv', mode='w') as csv_file:
    fieldnames = ['artist', 'title', 'genre', 'rating', 'date',
        'image', 'score', 'sp_artist', 'sp_popularity',
        'sp_followers', 'sp_artist_id']
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    csv_writer.writeheader()
    csv_writer.writerows(results)

with open('results/results_am.json', 'w') as json_file:
    json.dump(results, json_file, indent=4)
