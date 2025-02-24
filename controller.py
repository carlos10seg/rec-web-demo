import requests
from db_manager import DbManager
from config_reader import ConfigReader
from tmdb_proxy import TmdbProxy
import pandas as pd

class Controller:

    def setup_db(self):
        dbManager = DbManager()
        dbManager.setup_db()
    
    def get_recs_from_recserver(self, users, nr_recs, algo, items):
        config_reader = ConfigReader()
        base_url = config_reader.get_value("rec_server_url")
        #is_a_rec_request = True if algo == 'popular' or algo == 'topn' else False
        recs = []
        for userId in users:
           # if is_a_rec_request:
            url = f'{base_url}/algorithms/{algo}/recommendations?user_id={userId}&num_recs={nr_recs}'
            # else:
            #     url = f'{base_url}/algorithms/{algo}/predictions?user_id={userId}&items={items}'
            r = requests.get(url)
            data = r.json()
            #recs.append({'user': userId, 'recs': data['recommendations'] if is_a_rec_request else data['predictions']})
            recs.append({'user': userId, 'recs': data['recommendations']})
        return recs
        
        # print(data)
        # return data['recommendations']
    
    def get_movies(self, term):
        dbManager = DbManager()
        db_list = dbManager.get_movies(term)
        #for index, row in db_list.iterrows():
        return [{'id': m[1]['id'], 'label': m[1]['title'], 'value': m[1]['title']} for m in db_list.iterrows()]
        # db_list = [m for m in db_list if term in str.lower(m[1])]
        # return [{'id': m[0], 'label': m[1], 'value': m[1]} for m in db_list]

    def get_qprecs(self, algo, movies, nr_recs, items, user_id):
        dbManager = DbManager()        
        #user_id = dbManager.insert_and_get_min_user_id()
        rating_value = 5
        # remove all ratings from this user
        dbManager.remove_ratings(user_id)

        # insert ratings (value: 10) for user 0 for each movie
        for m in movies:
            dbManager.insert_rating(user_id, m, rating_value)
        
        # get recs
        all_recs = self.get_recs_from_recserver([user_id], nr_recs, algo, items)
        print(all_recs)
        for user_recs in all_recs:
            if user_recs['recs'] != None:
                for rec in user_recs['recs']:
                    rec['title'] = dbManager.get_movie(rec['item']).loc[0, 'title']
                    rec['image_url'] = self.get_image_url(rec['item'])

        return all_recs

    def get_current_user_id(self):
        dbManager = DbManager()        
        user_id = dbManager.insert_and_get_min_user_id()
        return user_id

    def get_image_url(self, movie_id):
        tmdb_proxy = TmdbProxy()
        links = pd.read_csv("data/links.csv", sep=',')
        tmdb_id = links[links['movieId'] == int(movie_id)]['tmdbId'].values[0]
        return tmdb_proxy.get_image_url(tmdb_id)