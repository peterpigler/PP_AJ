# coding=utf-8
# encoding=utf-8
"""
@scrapeTripInfo

@author: Peter Pigler
"""
import numpy
import pandas
import soup as soupOpen
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
HOTELTYPES = ["Best Value", "Boutique", "Budget", "Business", "Charming", "Classic", "Family-friendly", "Luxury",
              "Mid-range", "Quaint", "Quiet", "Romantic", "Trendy"]
PRICERANGE = [u'£', u"££ - £££", u"££££"]


def scrapeOverview(_city):
    citySplit = _city.split('-')
    # overview
    try:
        soup = soupOpen.open(soupOpen.TRIPADVISORCOM + "/Tourism-" + _city + "-Vacations.html")
    except:
        return
    entities = []
    try:
        entities = soup.find("div", {"class": "navLinks"}).find_all("li")  # find all overview type entities
    except:
        # return
        print "return"
    city_name = str(soup.find("h1", {"id": "HEADING"}).text)
    overviews = {"city_name": city_name, "city_id": str(citySplit[0])}
    for overview in entities:
        try:
            _label = str(overview.find("span", {"class": "typeName"}).text).lower().replace(' ','_')
        except:
            pass
        try:
            _qty = int(str(overview.find("span", {"class": "typeQty"}).text.strip("()")).replace(',', ''))
        except:
            _qty = -1
        if _label != "flights":
            try:
                _content = int(
                    str(overview.find("span", {"class": "contentCount"}).text.split(' ', 1)[0]).replace(',', ''))
            except:
                _content = -1
        else:
            try:
                _content = int(
                    str(overview.find("span", {"class": "contentCount"}).text.replace(u'\xa0', u' ')).split(' ')[
                        2].replace(',', ''))
            except:
                _content = -1
        if (_label != "flights") and (_label != "forum"):
            overviews.update({_label + '_quantity': _qty})
            overviews.update({_label + '_content': _content})
        else:
            overviews.update({_label + '_content': _content})
    print overviews
    dataframe_overviews = pandas.DataFrame(data=overviews, index=["key"])
    return dataframe_overviews


def scrapeAccommodations(_city):
    accommodations = [[], [], [], [], []]
    try:
        soup = soupOpen.open(soupOpen.TRIPADVISORUK + "/Hotels-" + _city + "-Hotels.html")
    except:
        return
    counts = soup.find_all("span" ,{"class": "tab_count"})
    if len(counts):
        tab_counts = [int(str(counts[0].text).strip("()")),int(str(counts[1].text).strip("()"))]
        for tab in tab_counts:
            while True:
                entities = soup.find_all("div", {"class": "listing easyClear  p13n_imperfect "}, limit = tab)  # find all hotel entities
                for accommodation in entities:
                    _id = str(accommodation["id"]).split('_')[1]
                    _name = str(accommodation.find('a', {"class": "property_title "}).text).replace('\n','')
                    try:
                        _reviews = int(
                            str(accommodation.find("span", {"class": "more review_count"}).text).split(' ', 1)[0].replace(',', ''))
                    except:
                        _reviews = -1
                    try:
                        _rating = float(str(accommodation.find("img", {"class": "sprite-ratings"})["alt"]).split(' ', 1)[0])
                    except:
                        _rating = -1.0
                    _category = -1
                    try:
                        tags = accommodation.find_all('a', {"class": "tag"})
                        for tag in tags:
                            if str(tag.text) in HOTELTYPES:
                                _category = HOTELTYPES.index(str(tag.text))
                    except:
                        pass
                    try:
                        accommodations[0].append(_id)
                        accommodations[1].append(_name)
                        accommodations[2].append(_reviews)
                        accommodations[3].append(_rating)
                        accommodations[4].append(_category)
                    except:
                        pass

                nextpage = soup.find("a", {"class": "nav next ui_button primary taLnk"})
                if nextpage:
                    _next = soupOpen.TRIPADVISORUK + str(nextpage["href"])
                    try:
                        soup = soupOpen.open(_next)
                    except:
                        break
                else:
                    break
            soup = soupOpen.open(soupOpen.TRIPADVISORUK + "/Hotels-" + _city + "-c2-Hotels.html")
    else:
        pass
    hotels = numpy.array(accommodations)
    print hotels.T
    dataframe_hotels = {"hotel_id": hotels[0], "hotel_name": hotels[1], "reviews": hotels[2], "ratings": hotels[3], "category": hotels[4]}
    dataframe_hotels = pandas.DataFrame(data=dataframe_hotels)
    return dataframe_hotels


def scrapeAttractions(_city):
    attractions = [[], [], [], []]
    try:
        soup = soupOpen.open(soupOpen.TRIPADVISORCOM + "/Attractions-" + _city + "-Activities.html")
    except:
        return
    while True:
        entities = soup.find_all("div", {"class": "entry"})  # find all attraction / activity type entities
        for activity in entities:
            try:
                _id = str(activity["id"]).split('_')[2]
                _name = str(activity.find('a').text).replace('\n','')
            except:
                break
            try:
                _reviews = int(
                    str(activity.find("span", {"class": "more"}).text).split(' ', 1)[0].replace("\n", '').replace(',',
                                                                                                                  ''))
            except:
                _reviews = -1
            try:
                _rating = float(str(activity.find("img", {"class": "sprite-ratings"})["alt"]).split(' ', 1)[0])
            except:
                _rating = -1.0
            try:
                attractions[0].append(_id)
                attractions[1].append(_name)
                attractions[2].append(_reviews)
                attractions[3].append(_rating)
            except:
                pass
        nextpage = soup.find("a", {"class": "nav next rndBtn ui_button primary taLnk"})
        if nextpage:
            _next = str(nextpage["href"])
            soup = soupOpen.open(soupOpen.TRIPADVISORCOM + _next)
        else:
            break
    attractions = numpy.array(attractions)
    print attractions.T
    dataframe_attractions = {"attraction_id": attractions[0], "attraction_name": attractions[1], "reviews": attractions[1], "ratings": attractions[2]}
    dataframe_attractions = pandas.DataFrame(data=dataframe_attractions)
    return dataframe_attractions


def scrapeRestaurants(_city):
    restaurants = [[], [], [], [], []]
    try:
        soup = soupOpen.open(soupOpen.TRIPADVISORUK + "/Restaurants-" + _city + ".html")
    except:
        return
    while True:
        entities = soup.find_all("div", class_="listing")
        for restaurant in entities:
            try:
                _id = str(restaurant["id"]).split('_')[1]
                _name = str(restaurant.find("h3", {"class", "title"}).text).replace('\n','')
            except:
                break
            try:
                _reviews = int(
                    str(restaurant.find("span", {"class": "reviewCount"}).text).split(' ', 1)[0].replace("\n", ''))
            except:
                _reviews = -1
            try:
                _rating = float(str(restaurant.find("img", {"class": "sprite-ratings"})["alt"]).split(' ', 1)[0])
            except:
                _rating = -1.0
            _price = -1
            try:
                rangetag = restaurant.find("span", {"class", "price_range"}).text.replace('\n', '')
                if rangetag in PRICERANGE:
                    _price = PRICERANGE.index(rangetag)
            except:
                pass
            try:
                restaurants[0].append(_id)
                restaurants[1].append(_name)
                restaurants[2].append(_reviews)
                restaurants[3].append(_rating)
                restaurants[4].append(_price)
            except:
                pass
        nextpage = soup.find("a", {"class": "nav next rndBtn ui_button primary taLnk"})
        if nextpage:
            _next = soupOpen.TRIPADVISORUK + str(nextpage["href"])
            soup = soupOpen.open(_next)
        else:
            break
    restaurants = numpy.array(restaurants)
    print restaurants.T
    dataframe_restaurants = {"restaurant_id": restaurants[0], "restaurant_name": restaurants[1],
                             "reviews": restaurants[2], "ratings": restaurants[3],"price": restaurants[4]}
    dataframe_restaurants = pandas.DataFrame(data=dataframe_restaurants)
    return dataframe_restaurants


def getUserAccommodationReviews(data_frame, city_id):
    hotel_list = data_frame["hotel_id"].tolist()
    city_users = [[], [], [], [], []]
    for hotel in hotel_list:
        print "acc_id: "+hotel
        try:    # open hotel_id link
            page = soupOpen.open(soupOpen.TRIPADVISORCOM+"/Hotel_Review-"+city_id+"-d"+hotel+"-Reviews.html")
        except:
            continue
        while True:
            reviews = page.find_all("div", {"class": "reviewSelector  "})
            for review in reviews:
                try:
                    city_users[1].append(str(review.find("div",
                        {"class": "username mo"}).text.encode('utf-8')).replace('\n', ''))
                    _rating = float(str(review.find("img", {"class": "sprite-rating_s_fill"})["alt"]).split(' ', 1)[0])
                    city_users[0].append(str(hotel))
                    city_users[2].append(_rating)
                    city_users[3].append(str(review.find("p", {"class", "partial_entry"}).text).replace('\n',''))
                    city_users[4].append(str(review.find("span" ,{"class","ratingDate relativeDate"})["title"]))
                except:
                    pass
            #is next page in _id hotel?
            nextpage = page.find("a", {"class": "nav next rndBtn ui_button primary taLnk"})
            if nextpage:
                next_page = "https://www.tripadvisor.com" + str(nextpage["href"])
                try:
                    page = soupOpen.open(next_page)
                except:
                    break
            else:
                break
    city_users_dataframe = pandas.DataFrame()
    try:
        city_users = numpy.array(city_users)
        city_users = {"hotel_id": city_users[0], "user": city_users[1], "rating": city_users[2]}
        city_users_dataframe = pandas.DataFrame(data=city_users)
    except:
        pass
    return city_users_dataframe


def getUserRestaurantReviews(data_frame, city_id):
    restaurant_list = data_frame["restaurant_id"].tolist()
    city_users = [[], [], []]   # 0. restaurant id, 1. user id, 2. rating
    for restaurant in restaurant_list:
        print "res id: "+restaurant
        try:    # open restaurant_id link
            page = soupOpen.open(soupOpen.TRIPADVISORUK+"/Restaurant_Review-"+city_id+"-d"+restaurant+"-Reviews.html")
        except:
            continue
        while True:
            reviews = page.find_all("div", {"class": "reviewSelector  "})
            for review in reviews:
                try:
                    city_users[1].append(str(review.find("div",
                        {"class": "username mo"}).text.encode('utf-8')).replace('\n',''))
                    city_users[0].append(str(restaurant))
                    _rating = float(str(review.find("img", {"class": "sprite-rating_s_fill"})["alt"]).split(' ',1)[0])
                    city_users[2].append(_rating)
                except:
                    pass
            # is next page in _id restaurant?
            nextpage = page.find("a", {"class": "nav next rndBtn ui_button primary taLnk"})
            if nextpage:
                next_page = soupOpen.TRIPADVISORUK+str(nextpage["href"])
                try:
                    page = soupOpen.open(next_page)
                except:
                    break
            else:
                break
    city_users_dataframe = pandas.DataFrame
    try:
        city_users = numpy.array(city_users)
        city_users = {"restaurant_id": city_users[0], "user": city_users[1], "rating": city_users[2]}
        city_users_dataframe = pandas.DataFrame(data=city_users)
    except:
        pass
    return city_users_dataframe

def getAccommodationFeatures(data_frame, city_id):
    hotel_list = data_frame["hotel_id"].tolist()
    result = []
    for hotel in hotel_list:
        print "acc id: "+hotel
        try:    # open hotel_id link
            page = soupOpen.open(soupOpen.TRIPADVISORCOM+"/Hotel_Review-"+city_id+"-d"+hotel+"-Reviews.html")
        except:
            continue
        print hotel
        # review var
        try:
            review_var = {"5": int(str(page.find("label", {"for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterRating_5"}).find_all("span")[2].text).replace(',','')),
                "4": int(str(page.find("label", {"for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterRating_4"}).find_all("span")[2].text).replace(',','')),
                "3": int(str(page.find("label", {"for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterRating_3"}).find_all("span")[2].text).replace(',','')),
                "2": int(str(page.find("label", {"for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterRating_2"}).find_all("span")[2].text).replace(',','')),
                "1": int(str(page.find("label", {"for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterRating_1"}).find_all("span")[2].text).replace(',',''))}

            # traveler type
            traveler_type = {"families": int(str(page.find("label", {"for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterSegment_Family"}).find("span").text).replace(',','').strip("()")),
                "couples": int(str(page.find("label", {"for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterSegment_Couples"}).find("span").text).replace(',','').strip("()")),
                "solo": int(str(page.find("label", {"for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterSegment_Solo"}).find("span").text).replace(',','').strip("()")),
                "business": int(str(page.find("label", {"for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterSegment_Business"}).find("span").text).replace(',','').strip("()")),
                "friends": int(str(page.find("label", {"for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterSegment_Friends"}).find("span").text).replace(',','').strip("()"))}

            # seasons
            seasons = {"spring": int(str(page.find("label", {"for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterSeasons_SPRING"}).find("span").text).replace(',','').strip("()")),
               "summer": int(str(page.find("label", {"for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterSeasons_SUMMER"}).find("span").text).replace(',','').strip("()")),
               "autumn": int(str(page.find("label", {"for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterSeasons_AUTUMN"}).find("span").text).replace(',','').strip("()")),
               "winter": int(str(page.find("label", {"for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterSeasons_WINTER"}).find("span").text).replace(',','').strip("()"))}

            features = {}
            amenities = page.find_all("div", {"class": "amenity_row"})
            for amenity in amenities:
                # get feature
                features[str(amenity.find("div", {"class": "amenity_hdr"}).text).replace(' ','_').replace('\n','')] = len(amenity.find_all("li"))
            # result.append({"hotel": hotel, "review_var": review_var, "traveler_type": traveler_type, "seasons": seasons, "features": features})
            row = {"hotel": hotel}
            row.update(review_var)
            row.update(traveler_type)
            row.update(seasons)
            row.update(features)
            result.append(row)
        except:
            continue

    return result

