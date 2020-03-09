import requests
from db_manager import DbManager

class Controller:
    
    def get_recs(self, users, nr_recs, algo, items):
        return self.get_recs_from_recserver(users, nr_recs, algo, items)

    def get_recs_from_recserver(self, users, nr_recs, algo, items):
#         # http://127.0.0.1:5001/lkpy/recommend/popular/2038/10
        recs = []
        for userId in users:
            url = f'http://127.0.0.1:5001/lkpy/recommend/{algo}/{userId}/{nr_recs}'
            r = requests.get(url)
            data = r.json()
            recs.append({'user': userId, 'recs': data['recommendations']})
        return recs
        
        print(data)
        return data['recommendations']
    
    def get_movies(self, term):
        dbManager = DbManager()
        db_list = dbManager.get_movies()
        db_list = [m for m in db_list if term in str.lower(m[1])]
        return [{'id': m[0], 'label': m[1], 'value': m[1]} for m in db_list]

