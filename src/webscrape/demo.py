# coding=utf-8
# encoding=utf-8
"""
@demo


@author: Peter Pigler
"""
import pandas

from scrapeTripInfo import scrapeOverview, scrapeAccommodations, scrapeAttractions, scrapeRestaurants, \
    getAccommodationFeatures, getUserAccommodationReviews, getUserRestaurantReviews
import scrapeTripInfo
from listGenerate import findCityList

def scrapeCity(_city, filename):
    # create pandas writer object
    writer = pandas.ExcelWriter(filename)
    # overviews
    overviews = scrapeOverview(_city)
    overviews.to_excel(writer, sheet_name="Overview")
    # hotels
    print "....accommodations...."
    hotels = scrapeAccommodations(_city)
    hotels.to_excel(writer, sheet_name="Hotels")
    # accommodation features
    print "........features...."
    features = getAccommodationFeatures(hotels,_city)
    pandas.DataFrame(features).to_excel(writer, sheet_name="Accommodation Features")
    print "........users...."
    reviews = getUserAccommodationReviews(hotels,_city)
    reviews.to_excel(writer, sheet_name="Accommodation Reviews")
    # attractions
    print "....attractions...."
    attractions= scrapeAttractions(_city)
    attractions.to_excel(writer, sheet_name="Attractions")
    # restaurants
    print "....restaurants...."
    restaurants = scrapeRestaurants(_city)
    restaurants.to_excel(writer, sheet_name="Restaurants")
    print"........users...."
    reviews = getUserRestaurantReviews(restaurants, _city)
    reviews.to_excel(writer, sheet_name="Restaurant Reviews")

    writer.save()
    return {"overview": overviews, "hotels": hotels, "restaurants": restaurants, "attractions": attractions}

import pydoc
"""
def stalkReviewer(filename):
    return

list = findCityList("Hungary")
print list
for city in list["city_id"]:
    scrapeCity(city,city+".xlsx")
"""
"""
locations = get_city_list()
for city in locations:
    _filename = city.split('-')[0].replace('/','')
    city_scrape(city,_filename+".xlsx")

get_users_hotel("g188671")


locations = getHungarianCityList()
Data = {"overview": [], "hotels": {}, "restaurants": {}, "attractions": {}}
for city in locations:
    _data = scrapeCity(city, city + ".xlsx")
    Data["overview"].append(_data["overview"])
    Data["hotels"][city] = _data["hotels"]
    Data["restaurants"][city] = _data["restaurants"]
    Data["attractions"][city] = _data["attractions"]

writer = pandas.ExcelWriter("Data.xlsx")
dataframeOverview = pandas.DataFrame()
for rows in Data["overview"]:
    dataframeOverview = dataframeOverview.append(pandas.DataFrame(rows, index=["key"]), ignore_index=True)
dataframeOverview.to_excel(writer, sheet_name="Overview")

locations = ["g274916", "g274904", "g274921", "g274919", "g274897", "g776248"]
for city in locations:
    features = getHotelFeatures(city)
    writer = pandas.ExcelWriter(city + "_hotel_features.xlsx")
    data = pandas.DataFrame(features)
    data.to_excel(writer)
    writer.close()

locations = getAccentsensitiveList()
locations = pandas.DataFrame(locations)
writer = pandas.ExcelWriter("EkezetesVarosok.xlsx")
locations.to_excel(writer)
writer.close()

result = getHotelFeatures("g274916")
writer = pandas.ExcelWriter("g274916_hotel_featuers.xlsx")
data = pandas.DataFrame(data=result)
data.to_excel(writer)
writer.close()


reader = pandas.read_excel("g274916_hotel_features.xlsx")

to_plot = reader[["About_the_property", "In_your_room", "Internet", "Room_types","Things_to_do", "Services"]]
labels = reader['hotel'].tolist()
#reader.plot.area(stacked = False)
ax=to_plot.plot.bar(rot=90, stacked=True)
ax.set_xticklabels(labels)
from matplotlib import pyplot as plt
plt.show()
"""


