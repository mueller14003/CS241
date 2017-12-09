from matplotlib import pyplot
import pandas
import matplotlib
matplotlib.get_backend()

data = pandas.read_csv("weather_year.csv")
# print(data)
# print(data.columns)
# print(data[["EDT", "Mean TemperatureF"]])
# # data.EDT.hist()
# matplotlib.pyplot.hist(data["Mean TemperatureF"])
# pyplot.show()
data.columns = ["date", "max_temp", "mean_temp", "min_temp", "max_dew",
                "mean_dew", "min_dew", "max_humidity", "mean_humidity",
                "min_humidity", "max_pressure", "mean_pressure",
                "min_pressure", "max_visibilty", "mean_visibility",
                "min_visibility", "max_wind", "mean_wind", "min_wind",
                "precipitation", "cloud_cover", "events", "wind_dir"]
# print(data.date.head())
empty = data.apply(lambda col: pandas.isnull(col))
# print(empty.events.head(10))
# print(data.events.head(10))
# print(data.dropna(subset=["events"]))


data.events = data.events.fillna("")
# print(data.events.head(10))


cover_temps = {}
for cover, cover_data in data.groupby("cloud_cover"):
    cover_temps[cover] = cover_data.mean_temp.mean()  # The mean mean temp! That's not very nice.......
# print(cover_temps)
#
# print(data.events.unique())

for event_kind in ["Rain", "Thunderstorm", "Fog", "Snow"]:
    col_name = event_kind.lower()  # Turn "Rain" into "rain", etc.
    data[col_name] = data.events.apply(lambda e: event_kind in e)
# print(data)
#
# print(data.rain)
# print(data.rain.sum())
# print(data[data.rain & data.snow])
# print()
# print()
# print()
# print()
# print()
# print()
# print()
# print()
# print()

pyplot.show(data.max_temp.tail().plot(kind="bar", rot=10))
