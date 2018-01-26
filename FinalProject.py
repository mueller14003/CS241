from matplotlib import pyplot as plt
import pandas as pd
import matplotlib as mpl
mpl.get_backend()
import numpy as np
import seaborn as sb

data = pd.read_csv("Data/movies.csv")


#print(data.rating.mean())
#print(data.rating.median())


data["mpaa_clean"] = data.mpaa.apply(lambda x: x.strip())
# pg_13 = data[data.mpaa.apply(lambda x: x.strip()) == "PG-13"]
# pg_13_year = pg_13.year.min()
# print(pg_13_year)


data["mpaa_clean"] = data["mpaa_clean"].apply(lambda x: x if x != "" else "NA")
# has_rating = [x for x in filter(lambda x: x != "NA", data["mpaa_clean"])]
# plt.hist(has_rating)
# plt.show()


# plt.hist(data.year, bins=112)
# plt.show()


genres = ['Action', 'Animation', 'Comedy', 'Drama', 'Documentary', 'Romance', 'Short']
# R_Movies = data[data["mpaa_clean"] == "R"]
# R_Movies_per_genre = {}
# Movies_per_genre = {}
# Percent_R_Movies = {}

# for genre in genres:
#     R_movies_in_genre = R_Movies[R_Movies[genre] == 1]
#     x = len(R_movies_in_genre[genre])
#     Movies_in_genre = data[data[genre] == 1]
#     y = len(Movies_in_genre[genre])
#     R_Movies_per_genre[genre] = x
#     Movies_per_genre[genre] = y
#     Percent_R_Movies[genre] = (x/y)*100

# X = np.arange(len(Movies_per_genre))
# ax = plt.subplot(111)
# ax.bar(X + .175, Movies_per_genre.values(), width=0.35, color='b', align='center')
# ax.bar(X - 0.175, R_Movies_per_genre.values(), width=0.35, color='r', align='center')
# ax.legend(('Movies', 'R Movies'))
# plt.xticks(X, Movies_per_genre.keys(), rotation="vertical")
# plt.title("R Movies vs Total Movies per Movie Genre", fontsize=17)
# plt.show()
#
#
# plt.bar(list(Percent_R_Movies.keys()), Percent_R_Movies.values())
# plt.xticks(rotation="vertical")
# plt.show()
#
#
# category = data[(~(data.Action == data.Comedy)) & (data.budget != " NA")]
# category["Category"] = ["Action" if ele == 1 else "Comedy" for ele in category["Action"]]
# category["budget"] = category["budget"].astype(int)
# plot = sb.boxplot("Category", "budget", data=category)
# plt.show(plot)


# comedy = category[category["Comedy"] == 1]
# print("Max Action: {}, Max Comedy: {}".format(category.budget.max(), comedy.budget.max()))


# dict_of_graphs = {}
#
# for genre in genres:
#     specific_genre = data[data[genre] == 1]
#     dict_of_graphs[genre] = sb.distplot(specific_genre.year, hist=False, label=genre)

# plt.title("Distribution of Movies by Genre Over Time", fontsize=17)
# plt.show(dict_of_graphs)
#
# long = {}
#
# for genre in genres:
#     specific_genre = data[(data[genre] == 1) & (data.length >= 100)]
#     long[genre] = sb.distplot(specific_genre.length, hist=False, label=genre)
#
# plt.title("Long Movies", fontsize=17)
# plt.show(long)


# long_movies = data[data.length >= 100]
#
# print(long_movies.min())
# print(long_movies.median())
# print(long_movies.max())
# print(long_movies.mean())




# long = {}
#
# for genre in genres:
#     specific_genre = long_movies[long_movies[genre] == 1]
#     long[genre] = sb.distplot(specific_genre)
#
# plt.title("Long Movies MPAA", fontsize=17)
# plt.show(long)


# good_movies = data[data.rating > 5]
#
# print(good_movies.min())
# print(good_movies.median())
# print(good_movies.max())
# print(good_movies.mean())
#
# good = {}
#
# for genre in genres:
#     specific_genre = good_movies[good_movies[genre] == 1]
#     good[genre] = sb.distplot(specific_genre.year, hist=False, label=genre)
#
# plt.title("Good movies", fontsize=17)
# plt.show(good)

print(data.columns)

rating = {}

for genre in genres:
    specific_genre = data[data[genre] == 1]
    rating[genre] = sb.distplot(specific_genre.rating, hist=False, label=genre)

plt.title("Movie Rating", fontsize=17)
plt.show(rating)




