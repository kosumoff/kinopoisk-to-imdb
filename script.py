import requests, bs4
import imdb
import re
import pandas as pd

def kinopoisk_to_imdb():
    cookie = ''  # paste cookie
    ia = imdb.IMDb()
    kp = pd.read_excel('movies/kinopoisk.xlsx')

    for i in kp.index:
        if str(kp['оригинальное название'][i]) == "nan":
            continue

        info = ia.search_movie(str(kp['оригинальное название'][i]))
        for item in info:
            print(f"ID: {item.movieID}, Title: {kp['оригинальное название'][i]}, Raiting: {kp['моя оценка'][i]}")

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
                'rating': str(kp['моя оценка'][i]),
                'auth': auth,
                'tracking_tag': 'title-maindetails',
                'pageId': 'tt' + str(item.movieID),
                'pageType': 'title',
                'subpageType': 'main'
            }
            response = requests.post('https://www.imdb.com/ratings/_ajax/title', headers=headers, data=data)
            break

if __name__ == '__main__':
    kinopoisk_to_imdb()
