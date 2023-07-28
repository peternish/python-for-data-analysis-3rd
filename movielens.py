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

mean_rating = data.pivot_table('rating', index = "title", columns = "gender", aggfunc = 'mean')

rating_by_title = data.groupby('title').size()
active_title = rating_by_title[rating_by_title >= 250]

mean_rating_active = mean_rating.iloc[active_title]
top_rating_female = mean_rating_active.sort_values(by='F',ascending=False)

#rating difference between men and women
mean_rating_active['dif'] = mean_rating_active['F'] - mean_rating_active['M']
top_rating_dif = mean_rating_active.sort_values(by='dif', ascending=False)