from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import urllib
from config_reader import ConfigReader
from pandas.io import sql
from datetime import datetime
import pandas as pd

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
 
    def setup_db(self):
        engine = create_engine(self.conn_string)
        sql.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY NOT NULL, userName varchar(100) NULL);', engine)
    
    def get_ratings(self):
        return sql.read_sql("SELECT t.user, t.item, t.rating, timestamp FROM rating t;", create_engine(self.conn_string))

    def get_movies(self, term):
        return sql.read_sql("SELECT id, title, genres FROM items WHERE LOWER(title) LIKE '%{term}%';".format(term=term.lower()), create_engine(self.conn_string))

    def get_movie(self, id):
        return sql.read_sql("SELECT title, genres FROM items WHERE id = {id};".format(id=id), create_engine(self.conn_string))

    def insert_rating(self, user_id, movie_id, rating_value):        
        sql.execute("INSERT INTO rating VALUES ({user}, {item}, {rating}, '{timestamp}')".format(
                    user=user_id,
                    item=movie_id,
                    rating=rating_value,
                    timestamp=int(str(datetime.timestamp(datetime.now()))[:10]),
                    ), create_engine(self.conn_string))

    def remove_ratings(self, user_id):
        sql.execute("DELETE FROM rating t WHERE t.user = {user}".format(
                    user=user_id), create_engine(self.conn_string))

    def insert_and_get_min_user_id(self):
        db_list = sql.read_sql("SELECT MIN(id) as user FROM users;", create_engine(self.conn_string))
        #min_user_id = [m[1]['user'] for m in db_list.iterrows()][0]
        min_user_id = db_list.iloc[0]['user']
        if min_user_id is None:
            min_user_id = 0
        else:
            min_user_id = int(min_user_id)
        user_id = int(min_user_id - 1)
        sql.execute("INSERT INTO users VALUES ({user}, '')".format(user=user_id), create_engine(self.conn_string))
        return user_id
    