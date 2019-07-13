import requests, bs4
import imdb
import re

movies = {'Interstellar': 10, 'Titanic': 10, 'Inception': 9, 'Alita: Battle Angel': 7}
ia = imdb.IMDb()
cookie = '' # paste cookie

for key, value in movies.items():
    info = ia.search_movie(key)
    for item in info:
        print(f"ID: {item.movieID}, Title: {key}, Raiting: {value}")
        # get auth
        headers = {'cookie': cookie}
        res = requests.get('https://www.imdb.com/title/tt' + str(item.movieID) + '/', headers=headers)
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        rate_class = soup.select('.star-rating-widget')
        auth = ((re.search('data-auth="(.+?)"', str(rate_class))).group(1))

        # rate movie
        headers = {'cookie': cookie, 'referer': 'https://www.imdb.com/title/tt' + str(item.movieID) + '/'}
        data = {
            'tconst': 'tt' + str(item.movieID),
            'rating': str(value),
            'auth': auth,
            'tracking_tag': 'title-maindetails',
            'pageId': 'tt' + str(item.movieID),
            'pageType': 'title',
            'subpageType': 'main'
        }
        response = requests.post('https://www.imdb.com/ratings/_ajax/title', headers=headers, data=data)
        break
