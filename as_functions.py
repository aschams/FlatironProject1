import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_context("talk")


def OHE_genres(movie_list):
    movie_list['genres_list'] = movie_list.genres.str.split(',')
    s = movie_list.apply(lambda x: pd.Series(x['genres_list']),
                                             axis=1).stack().reset_index(level=1, drop=True)
    s.name = 'Genres'
    imdb_genres = movie_list.join(s).copy()
    genres_dummies = pd.get_dummies(imdb_genres.Genres).sum(level=0)
    ml = movie_list.join(genres_dummies).drop(['genres', 'genres_list'], axis=1)
    return ml

def plot_most_popular_people(df, role, category, frequency=3, n=10, figsize=(10,6)):
    fig = plt.figure(figsize=(10,6))
    ax = fig.add_subplot(111)
    people = df[df[role] == 1]
    vc = people['primary_name'].value_counts()
    infrequent_people = vc[vc <= frequency].index
    people.set_index('primary_name', inplace=True)
    frequent_people = people.drop(infrequent_people)
    most_popular_people = frequent_people.groupby('primary_name')[category].mean().sort_values(ascending=False).head(n)
    sns.barplot(x=most_popular_people.index, y=most_popular_people, ax=ax)
    plt.xticks(rotation=30)
    plt.xlabel(str(role + "s name").title())
    plt.ylabel(category.title())
    plt.title(str(role + 's sorted by average ' + category).title())
