from config_reader import ConfigReader
import requests

class TmdbProxy:
    def __init__(self):
        reader = ConfigReader()
        self.tmdb_search_url = reader.get_value('tmdb_search_url')
        self.tmdb_images_url = reader.get_value('tmdb_images_url')
        self.tmdb_get_image_url = reader.get_value('tmdb_get_image_url')

    def get_image_url(self, movie_name, movie_year):
        movie_id = None
        # 1) Get movie id
        movies = requests.get(self.tmdb_search_url + movie_name).json()
        if len(movies['results']) > 0:
            for r in movies['results']:
                if movie_year in r['release_date']:
                    movie_id = r['id']
                    break
        
        # 2) Get image file path
        images = requests.get(self.tmdb_images_url.replace('<movieId>', str(movie_id))).json()
        file_path = None
        if 'posters' in images and len(images['posters']) > 0:
            file_path = images['posters'][0]['file_path']
        elif 'backdrops' in images and len(images['backdrops']) > 0:
            file_path = images['backdrops'][0]['file_path']

        # 3) Get image 
        if file_path != None:
            return self.tmdb_get_image_url.replace('<image>', file_path)
