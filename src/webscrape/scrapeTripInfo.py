# coding=utf-8
# encoding=utf-8
"""
@lib: scrapeTripInfo

@author: Peter Pigler
"""
import numpy
import pandas
import soup as soupOpen
import sys
from unidecode import unidecode

reload(sys)
sys.setdefaultencoding('utf-8')
HOTELTYPES = ["Best Value", "Boutique", "Budget", "Business", "Charming", "Classic", "Family-friendly", "Luxury",
              "Mid-range", "Quaint", "Quiet", "Romantic", "Trendy"]
PRICERANGE = [u'£', u"££ - £££", u"££££"]


def scrapeOverview(_city):
    """
    Parameters
    ----
    _city: String
        The _city_id of the analysable city

    Description
    ----
    Returns a Pandas Dataframe, with the city's first step-depth analise, including name of the
    given city_id, contents and quantities of accommodations, restaurants, attractions.

    Can handle multi-paged sites.

    Returns
    -----
    d: Dataframe
    """
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
    overviews = {"CITY_NAME": city_name, "CITY_ID": str(citySplit[0])}
    for overview in entities:
        try:
            _label = str(overview.find("span", {"class": "typeName"}).text).capitalize().replace(' ','_')
        except:
            pass
        try:
            _qty = int(str(overview.find("span", {"class": "typeQty"}).text.strip("()")).replace(',', ''))
        except:
            _qty = numpy.nan
        if _label != "flights":
            try:
                _content = int(
                    str(overview.find("span", {"class": "contentCount"}).text.split(' ', 1)[0]).replace(',', ''))
            except:
                _content = numpy.nan
        else:
            try:
                _content = int(
                    str(overview.find("span", {"class": "contentCount"}).text.replace(u'\xa0', u' ')).split(' ')[
                        2].replace(',', ''))
            except:
                _content = numpy.nan
        if (_label != "flights") and (_label != "forum"):
            overviews.update({_label + '_QUANTITY': _qty})
            overviews.update({_label + '_CONTENT': _content})
        else:
            overviews.update({_label + '_CONTENT': _content})
    print overviews
    dataframe_overviews = pandas.DataFrame(data=overviews, index=["key"])
    return dataframe_overviews


def scrapeAccommodations(_city):
    """
    Parameters
    ----
    _city: String
        The _city_id of the analysable city

    Description
    ----
    Returns a Pandas Dataframe, with the city's second step-depth analise, including name of the
    accommodations found in _city, review quantities and ratings and accommodation types.

    Can handle multi-paged sites.

    Returns
    -----
    d: Dataframe
    """
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
                        _reviews = numpy.nan
                    try:
                        _rating = float(str(accommodation.find("span", {"class": "ui_bubble_rating"})["alt"]).split(' ', 1)[0])
                    except:
                        _rating = numpy.nan
                    _category = numpy.nan
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
    dataframe_hotels = {"ACCOMMODATION_ID": hotels[0], "ACCOMMODATION_NAME": hotels[1], "REVIEWS": hotels[2], "RATINGS": hotels[3], "CATEGORY": hotels[4]}
    dataframe_hotels = pandas.DataFrame(data=dataframe_hotels)
    return dataframe_hotels


def scrapeAttractions(_city):
    """
        Parameters
        ----
        _city: String
            The _city_id of the analysable city

        Description
        ----
        Returns a Pandas Dataframe, with the city's second step-depth analise, including name of the
        attractions found in _city, review quantities and ratings.

        Can handle multi-paged sites.

        Returns
        -----
        d: Dataframe
        """
    attractions = [[], [], [], [], []]
    try:
        soup = soupOpen.open(soupOpen.TRIPADVISORUK + "/Attractions-" + _city + "-Activities.html")
    except:
        return
    while True:
        entities = soup.find_all("div", {"class": "element_wrap"})  # find all attraction / activity type entities
        for activity in entities:
            try:
                _id = unidecode(activity.find('div', {'class': 'entry'})['id']).split('_')[2]
                _name = unidecode(activity.find('div', {'class': 'property_title'}).find('a').text).replace('\n','')
            except:
                continue
            try:
                _reviews = int(
                    str(activity.find("span", {"class": "more"}).text).split(' ', 1)[0].replace("\n", '').replace(',',
                                                                                                                  ''))
            except:
                _reviews = numpy.nan
            try:
                _rating = float(str(activity.find("img", {"class": "sprite-ratings"})["alt"]).split(' ', 1)[0])
            except:
                _rating = numpy.nan
            try:
                _category = unidecode(activity.find('div', {'class': 'p13n_reasoning_v2'}).text).replace('\n','')
            except:
                _category = numpy.nan
            try:
                attractions[0].append(_id)
                attractions[1].append(_name)
                attractions[2].append(_category)
                attractions[3].append(_reviews)
                attractions[4].append(_rating)
            except:
                pass
        nextpage = soup.find("a", {"class": "nav next rndBtn ui_button primary taLnk"})
        if nextpage:
            _next = str(nextpage["href"])
            soup = soupOpen.open(soupOpen.TRIPADVISORUK + _next)
        else:
            break
    attractions = numpy.array(attractions)
    print attractions.T
    dataframe_attractions = {"ATTRACTION_ID": attractions[0], "ATTRACTION_NAME": attractions[1], "CATEGORY": attractions[2], "REVIEWS": attractions[3], "RATINGS": attractions[4]}
    dataframe_attractions = pandas.DataFrame(data=dataframe_attractions)
    dataframe_attractions.replace(0,numpy.nan)
    return dataframe_attractions


def scrapeRestaurants(_city):
    """
        Parameters
        ----
        _city: String
            The _city_id of the analysable city

        Description
        ----
        Returns a Pandas Dataframe, with the city's second step-depth analise, including name of the
        restaurants found in _city, review quantities and ratings, restaurant types.

        Can handle multi-paged sites.

        Returns
        -----
        d: Dataframe
        """
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
                    float(str(restaurant.find("span", {"class": "reviewCount"}).text).split(' ', 1)[0].replace("\n", '')))
            except:
                _reviews = numpy.nan
            try:
                _rating = float(str(restaurant.find("img", {"class": "sprite-ratings"})["alt"]).split(' ', 1)[0])
            except:
                _rating = numpy.nan
            _price = numpy.nan
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
    dataframe_restaurants = {"RESTAURANT_ID": restaurants[0], "RESTAURANT_NAME": restaurants[1],
                             "REVIEWS": restaurants[2], "RATINGS": restaurants[3],"PRICE": restaurants[4]}
    dataframe_restaurants = pandas.DataFrame(data=dataframe_restaurants)
    dataframe_restaurants.replace(0, numpy.nan)
    return dataframe_restaurants


def getAccommodationFeatures(data_frame, city_id):
    """
        Parameters
        ----
        data_frame: Dataframe
            The given city accommodation dataframe
        _city: String
            The _city_id of the analysable city

        Description
        ----
        Returns a Pandas Dataframe, with the city's third step-depth analise, including accommodations'
        features. For further notations see FEATURES.

        Can handle multi-paged sites.

        Returns
        -----
        d: Dataframe
        """
    hotel_list = data_frame["ACCOMMODATION_ID"].tolist()
    result = []
    for hotel in hotel_list:
        print "acc id: "+hotel
        try:    # open hotel_id link
            page = soupOpen.open(soupOpen.TRIPADVISORCOM+"/Hotel_Review-"+city_id+"-d"+hotel+"-Reviews.html")
        except:
            continue
        # review var
        try:
            review_var = {"5": int(str(page.find("label", {"for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterRating_5"}).find_all("span")[2].text).replace(',','')),
                "4": int(str(page.find("label", {"for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterRating_4"}).find_all("span")[2].text).replace(',','')),
                "3": int(str(page.find("label", {"for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterRating_3"}).find_all("span")[2].text).replace(',','')),
                "2": int(str(page.find("label", {"for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterRating_2"}).find_all("span")[2].text).replace(',','')),
                "1": int(str(page.find("label", {"for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterRating_1"}).find_all("span")[2].text).replace(',',''))}

            # traveler type
            traveler_type = {"FAMILIES": int(str(page.find("label", {"for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterSegment_Family"}).find("span").text).replace(',','').strip("()")),
                "COUPLES": int(str(page.find("label", {"for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterSegment_Couples"}).find("span").text).replace(',','').strip("()")),
                "SOLO": int(str(page.find("label", {"for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterSegment_Solo"}).find("span").text).replace(',','').strip("()")),
                "BUSINESS": int(str(page.find("label", {"for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterSegment_Business"}).find("span").text).replace(',','').strip("()")),
                "FRIENDS": int(str(page.find("label", {"for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterSegment_Friends"}).find("span").text).replace(',','').strip("()"))}

            # seasons
            seasons = {"SPRING": int(str(page.find("label", {"for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterSeasons_SPRING"}).find("span").text).replace(',','').strip("()")),
               "SUMMER": int(str(page.find("label", {"for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterSeasons_SUMMER"}).find("span").text).replace(',','').strip("()")),
               "AUTUMN": int(str(page.find("label", {"for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterSeasons_AUTUMN"}).find("span").text).replace(',','').strip("()")),
               "WINTER": int(str(page.find("label", {"for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterSeasons_WINTER"}).find("span").text).replace(',','').strip("()"))}

            features = {}
            amenities = page.find_all("div", {"class": "amenity_row"})
            for amenity in amenities:
                # get feature
                features[str(amenity.find("div", {"class":
                  "amenity_hdr"}).text).replace(' ','_').replace('\n','').capitalize()] = len(amenity.find_all("li"))
            # result.append({"hotel": hotel, "review_var": review_var, "traveler_type": traveler_type, "seasons": seasons, "features": features})
            row = {"ACCOMMODATION_ID": hotel}
            row.update(review_var)
            row.update(traveler_type)
            row.update(seasons)
            row.update(features)
            result.append(row)
        except:
            continue

    return result


def scrapethis(_city, _acc):
    users = [[], [], [], [], []]
    # open
    try:
        page = soupOpen.open(soupOpen.TRIPADVISORUK+'/Hotel_Review-'+_city+'-d'+_acc+'-Reviews.html')
    except:
        return
    # scrape through reviews
    while True:
        reviews = page.find_all('div' ,{'class': 'reviewSelector  '})
        nextpage = page.find("a", {"class": "nav next rndBtn ui_button primary taLnk"})
        for review in reviews:
            try:
                if len(review.contents) > 1:
                    users[1].append(unidecode(review.find('div', {'class': 'username'}).text).replace('\n',''))
            except:
                print review
        if nextpage:
            next_page = "https://www.tripadvisor.com" + str(nextpage["href"])
            try:
                page = soupOpen.open(next_page)
            except:
                break
        else:
            break
    return users


def getUserAccommodationReviews(data_frame, city_id):
    """
        Parameters
        ----
        data_frame: Dataframe
            The given city accommodation dataframe
        _city: String
            The _city_id of the analysable city

        Description
        ----
        Returns a Pandas Dataframe, with the city's third step-depth analise, including accommodations'
        user reviews with ratings, review-text, date. Further step is to use sentiment-analysis

        Can handle multi-paged sites.

        Returns
        -----
        d: Dataframe
        """
    hotel_list = data_frame["ACCOMMODATION_ID"].tolist()
    city_users = [[], [], [], [], []]
    for hotel in hotel_list:
        print "acc_id: "+hotel
        try:    # open hotel_id link
            page = soupOpen.open(soupOpen.TRIPADVISORUK+"/Hotel_Review-"+city_id+"-d"+hotel+"-Reviews.html")
        except:
            continue
        while True:
            reviews = page.find_all("div", {"class": "reviewSelector  "})
            for review in reviews:
                if len(review.contents) > 1:
                    city_users[1].append(unidecode(review.find('div', {'class': 'username'}).text).replace('\n',''))
                    try:
                        _rating = float(str(review.find("div", {"class", "rating"}).find("span")["class"][1]).split('_')[1])
                    except:
                        _rating = numpy.nan
                    city_users[0].append(str(hotel))
                    city_users[2].append(_rating)
                    city_users[3].append(str(review.find("p", {"class", "partial_entry"}).text).replace('\n',''))
                    try:
                        city_users[4].append(str(review.find("span" ,{"class","ratingDate relativeDate"})["title"]).replace('\n',''))
                    except:
                        city_users[4].append(str(review.find("span", {"class", "ratingDate"}).text).strip('Reviewed ').replace('\n',''))
            #is next page in _id hotel?
            nextpage = page.find("a", {"class": "nav next rndBtn ui_button primary taLnk"})
            if nextpage:
                next_page = "https://www.tripadvisor.co.uk" + str(nextpage["href"])
                try:
                    page = soupOpen.open(next_page)
                except:
                    break
            else:
                break
    city_users_dataframe = pandas.DataFrame()
    try:
        city_users = numpy.array(city_users)
        city_users = {"ACCOMMODATION_ID": city_users[0], "USER_ID": city_users[1], "RATING": city_users[2], "TEXT": city_users[3], "DATE": city_users[4]}
        city_users_dataframe = pandas.DataFrame(data=city_users)
        city_users_dataframe.replace(0, numpy.nan)
    except:
        pass
    return city_users_dataframe


def getUserRestaurantReviews(data_frame, city_id):
    """
        Parameters
        ----
        data_frame: Dataframe
            The given city restaurant dataframe
        _city: String
            The _city_id of the analysable city

        Description
        ----
        Returns a Pandas Dataframe, with the city's third step-depth analise, including restaurants'
        user reviews with ratings, review-text, date. Further step is to use sentiment-analysis

        Can handle multi-paged sites.

        Returns
        -----
        d: Dataframe
        """
    restaurant_list = data_frame["RESTAURANT_ID"].tolist()
    city_users = [[], [], [], [], []]   # 0. restaurant id, 1. user id, 2. rating, 3. text, 4. date
    for restaurant in restaurant_list:
        print "res id: "+restaurant
        try:    # open restaurant_id link
            page = soupOpen.open(soupOpen.TRIPADVISORUK+"/Restaurant_Review-"+city_id+"-d"+restaurant+"-Reviews.html")
        except:
            continue
        while True:
            reviews = page.find_all("div", {"class": "reviewSelector  "})
            for review in reviews:
                if len(review.contents) > 1:
                    try:
                        city_users[1].append(unidecode(review.find('div', {'class': 'username'}).text).replace('\n', ''))
                    except:
                        city_users[1].append(numpy.nan)
                    city_users[0].append(str(restaurant))
                    _rating = float(str(review.find("img", {"class": "sprite-rating_s_fill"})["alt"]).split(' ',1)[0])
                    city_users[2].append(_rating)
                    city_users[3].append(str(review.find("p", {"class", "partial_entry"}).text).replace('\n', ''))
                    try:
                        city_users[4].append(str(review.find("span", {"class",
                              "ratingDate"})["title"]).replace('NEW',''))
                    except:
                        city_users[4].append(str(review.find("span", {"class",
                              "ratingDate"}).text).strip('Reviewed ').replace('NEW',''))
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
    try:
        city_users = numpy.array(city_users)
        city_users = {"RESTAURANT_ID": city_users[0], "USER_ID": city_users[1], "RATING": city_users[2], "TEXT": city_users[3], "DATE": city_users[4]}
        city_users_dataframe = pandas.DataFrame(data=city_users)
        city_users_dataframe.replace(0, numpy.nan)
    except:
        city_users_dataframe = pandas.DataFrame()
    return city_users_dataframe


def getUserAttractionReviews(data_frame, city_id):
    attraction_list = data_frame['ATTRACTION_ID'].tolist()
    city_users = [[], [], [], [], []]
    for attraction in attraction_list:
        print "attraction id: "+attraction
        try:
            page = soupOpen.open(soupOpen.TRIPADVISORUK+'/Attraction_Review-'+city_id+'-d'+attraction+'-Reviews.html')
            eng_reviews = int(
                page.find('label', {'for': 'taplc_prodp13n_hr_sur_review_filter_controls_0_filterLang_en'}).find('span').text.strip(
                    "()").replace(',',''))
        except:
            continue
        # Optimized deep-scrape - get features here
        while eng_reviews > 0:
            reviews = page.find_all('div', {'class': 'reviewSelector'})
            for review in reviews:
                try:
                    city_users[1].append(unidecode(review.find('div', {'class': 'username'}).text).replace('\n', ''))
                except:
                    city_users[1].append(numpy.nan)
                city_users[0].append(str(attraction))
                _rating = float(str(review.find("img", {"class": "sprite-rating_s_fill"})['alt']).split(' ',1)[0])
                city_users[2].append(_rating)
                city_users[3].append(unidecode(review.find("p", {"class", "partial_entry"}).text).replace('\n', ''))
                try:
                    city_users[4].append(str(review.find("span", {"class",
                                                                  "ratingDate"})["title"]).replace('NEW', ''))
                except:
                    city_users[4].append(str(review.find("span", {"class",
                                                                  "ratingDate"}).text).strip('Reviewed ').replace('NEW',
                                                                                                                  ''))
                    # is next page in _id attraction?
            nextpage = page.find("a", {"class": "nav next rndBtn ui_button primary taLnk"})
            if nextpage:
                next_page = soupOpen.TRIPADVISORUK + str(nextpage["href"])
                try:
                    page = soupOpen.open(next_page)
                except:
                    break
            else:
                break
    try:
        city_users = numpy.array(city_users)
        city_users = {"ATTRACTION_ID": city_users[0], "USER_ID": city_users[1], "RATING": city_users[2], "TEXT": city_users[3], "DATE": city_users[4]}
        city_users_dataframe = pandas.DataFrame(data=city_users)
        city_users_dataframe.replace(0, numpy.nan)
    except:
        city_users_dataframe = pandas.DataFrame()
    return city_users_dataframe


def getDeepRestaurants(data_frame, city_id):
    """
    Parameters
    ----
    data_frame: Dataframe
        The given city restaurant dataframe
    _city: String
        The _city_id of the analysable city

    Description
    ----
    Returns a Pandas Dataframe, with the city's first versioned optimized-deep details including restaurants'
    user reviews with ratings, review-text, date, user type, season and overall rating. Gets full
    text review, for sentiment-analysis.

    Can handle multi-paged sites.

    Returns
    -----
    d: Dataframe
    """
    restaurant_list = data_frame["RESTAURANT_ID"].tolist()
    city_users = [[], [], [], [], []]  # 0. restaurant id, 1. user id, 2. rating
    city_segments = []    # 0. overall rating, 1. user type, 2. season

    for restaurant in restaurant_list:
        print "res id: " + restaurant
        try:  # open restaurant_id link
            page = soupOpen.open(
                soupOpen.TRIPADVISORUK + "/Restaurant_Review-" + city_id + "-d" + restaurant + "-Reviews.html")
        except:
            continue
        try:
            review_var = {"5": int(str(page.find("label", {
                "for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterRating_5"}).find_all("span")[
                                   2].text).replace(',', '')),
                  "4": int(str(page.find("label", {
                      "for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterRating_4"}).find_all(
                      "span")[2].text).replace(',', '')),
                  "3": int(str(page.find("label", {
                      "for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterRating_3"}).find_all(
                      "span")[2].text).replace(',', '')),
                  "2": int(str(page.find("label", {
                      "for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterRating_2"}).find_all(
                      "span")[2].text).replace(',', '')),
                  "1": int(str(page.find("label", {
                      "for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterRating_1"}).find_all(
                      "span")[2].text).replace(',', ''))}

            # traveler type
            traveler_type = {"families": int(str(page.find("label", {
                "for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterSegment_Family"}).find(
                "span").text).replace(',', '').strip("()")),
                 "couples": int(str(page.find("label", {
                     "for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterSegment_Couples"}).find(
                     "span").text).replace(',', '').strip("()")),
                 "solo": int(str(page.find("label", {
                     "for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterSegment_Solo"}).find(
                     "span").text).replace(',', '').strip("()")),
                 "business": int(str(page.find("label", {
                     "for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterSegment_Business"}).find(
                     "span").text).replace(',', '').strip("()")),
                 "friends": int(str(page.find("label", {
                     "for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterSegment_Friends"}).find(
                     "span").text).replace(',', '').strip("()"))}

            # seasons
            seasons = {"spring": int(str(page.find("label", {
                "for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterSeasons_SPRING"}).find(
                "span").text).replace(',', '').strip("()")),
                   "summer": int(str(page.find("label", {
                       "for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterSeasons_SUMMER"}).find(
                       "span").text).replace(',', '').strip("()")),
                   "autumn": int(str(page.find("label", {
                       "for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterSeasons_AUTUMN"}).find(
                       "span").text).replace(',', '').strip("()")),
                   "winter": int(str(page.find("label", {
                       "for": "taplc_prodp13n_hr_sur_review_filter_controls_0_filterSeasons_WINTER"}).find(
                       "span").text).replace(',', '').strip("()"))}

            row = {"RESTAURANT_ID": restaurant}
            row.update(review_var)
            row.update(traveler_type)
            row.update(seasons)
            city_segments.append(row)
        except:
            pass
        while True:
            reviews = page.find_all("div", {"class": "reviewSelector  "})
            for review in reviews:
                try:
                    city_users[1].append(str(review.find("div",
                                                         {'class": "username'}).text.encode('utf-8')).replace('\n',
                                                                                                                 ''))
                    city_users[0].append(str(restaurant))
                    _rating = float(str(review.find("img", {"class": "sprite-rating_s_fill"})["alt"]).split(' ', 1)[0])
                    city_users[2].append(_rating)
                except:
                    pass
            # is next page in _id restaurant?
            nextpage = page.find("a", {"class": "nav next rndBtn ui_button primary taLnk"})
            if nextpage:
                next_page = soupOpen.TRIPADVISORUK + str(nextpage["href"])
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
        city_users_dataframe.replace(0, numpy.nan)
    except:
        pass
    city_segments_dataframe = pandas.DataFrame()
    try:
        city_segments_dataframe = pandas.DataFrame(city_segments).replace(0,numpy.nan)
    except:
        pass
    return city_users_dataframe, city_segments_dataframe