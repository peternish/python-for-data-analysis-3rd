import pandas as pd
import numpy as np
import seaborn as sns

mnames = ['movie_id', 'title', 'genre']
movies = pd.read_table('datasets/movielens/movies.dat', sep='::', names=mnames, header=None)

unames = ['user_id', 'gender', 'age', 'occupation', 'zipcode']
users = pd.read_table('datasets/movielens/users.dat', sep='::', names=unames, header=None)

rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_table('datasets/movielens/ratings.dat', sep='::', names=rnames, header=None)

data = pd.merge(users, pd.merge(ratings, movies))

