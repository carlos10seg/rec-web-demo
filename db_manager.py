from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import urllib
from config_reader import ConfigReader
from pandas.io import sql
from datetime import datetime

class DbManager:
    def __init__(self):
        reader = ConfigReader()
        db_connection = reader.get_value("db_connection")        
        self.conn_string = '{db_engine}{connector}://{user}:{password}@{server}/{database}'.format(
            db_engine=db_connection['db_engine'],
            connector=db_connection['connector'],
            user=db_connection['user'],
            password=db_connection['password'],
            server=db_connection['server'],
            database=db_connection['database'])
 
    def get_ratings(self):
        return sql.read_sql("SELECT userId, itemId, rating, timestamp FROM ratings;", create_engine(self.conn_string))

    def get_movies(self, term):
        return sql.read_sql("SELECT movieId, title, genres FROM movies WHERE title LIKE '%{term}%';".format(term=term), create_engine(self.conn_string))

    def get_movie(self, id):
        return sql.read_sql("SELECT title, genres FROM movies WHERE movieId = {id};".format(id=id), create_engine(self.conn_string))

    def get_links(self):
        return sql.read_sql("SELECT movieId, imdbId, tmdbId FROM links;", create_engine(self.conn_string))

    def insert_rating(self, user_id, movie_id, rating_value):        
        sql.execute("INSERT INTO ratings VALUES ({userId}, {itemId}, {rating}, '{timestamp}')".format(
                    userId=user_id,
                    itemId=movie_id,
                    rating=rating_value,
                    timestamp=datetime.timestamp(datetime.now()),
                    ), create_engine(self.conn_string))

    def remove_ratings(self, user_id):
        sql.execute("DELETE FROM ratings WHERE userId = {userId}".format(
                    userId=user_id), create_engine(self.conn_string))

    def insert_and_get_min_user_id(self):
        db_list = sql.read_sql("SELECT MIN(userId) as userId FROM users;", create_engine(self.conn_string))
        #min_user_id = [m[1]['userId'] for m in db_list.iterrows()][0]
        min_user_id = db_list.iloc[0]['userId']
        user_id = int(min_user_id - 1)
        sql.execute("INSERT INTO users(userId) VALUES ({userId})".format(userId=user_id), create_engine(self.conn_string))
        return user_id
    