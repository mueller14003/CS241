from matplotlib import pyplot as plt
import pandas as pd
import matplotlib as mpl
mpl.get_backend()
import numpy as np


data = pd.read_csv("Data/movies.csv")
# print(data)

print(data.columns)

print(data.rating.mean())

print(data.rating.median())

data["mpaa_clean"] = data.mpaa.apply(lambda x: x.strip())

pg_13 = data[data.mpaa.apply(lambda x: x.strip()) == "PG-13"]

pg_13_year = pg_13.year.min()

print(pg_13_year)

data["mpaa_clean"] = data["mpaa_clean"].apply(lambda x: x if x != "" else "NA")

has_rating = [x for x in filter(lambda x: x != "NA", data["mpaa_clean"])]

plt.hist(has_rating)

plt.show()

plt.hist(data.year, bins=112)

plt.show()

genres = ['Action', 'Animation', 'Comedy', 'Drama', 'Documentary', 'Romance', 'Short']

R_Movies = data[data["mpaa_clean"] == "R"]

R_Movies_per_genre = {}

Movies_per_genre = {}

Percent_R_Movies = {}

for genre in genres:
    R_movies_in_genre = R_Movies[R_Movies[genre] == 1]
    x = len(R_movies_in_genre[genre])
    Movies_in_genre = data[data[genre] == 1]
    y = len(Movies_in_genre[genre])
    R_Movies_per_genre[genre] = x
    Movies_per_genre[genre] = y
    Percent_R_Movies[genre] = (x/y)*100

X = np.arange(len(Movies_per_genre))
ax = plt.subplot(111)
ax.bar(X + .175, Movies_per_genre.values(), width=0.35, color='b', align='center')
ax.bar(X - 0.175, R_Movies_per_genre.values(), width=0.35, color='r', align='center')
ax.legend(('Movies', 'R Movies'))
plt.xticks(X, Movies_per_genre.keys(), rotation="vertical")
plt.title("R Movies vs Total Movies per Movie Genre", fontsize=17)
plt.show()

plt.bar(list(Percent_R_Movies.keys()), Percent_R_Movies.values())
plt.show()

print(data.columns)


