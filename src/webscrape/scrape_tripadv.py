from bs4 import BeautifulSoup
import urllib2
import numpy
import pandas

HOTELTYPES = ["Best Value","Boutique","Budget","Business","Charming","Classic","Family-friendly","Luxury","Mid-range", "Quaint", "Quiet", "Romantic","Trendy"]
PRICERANGE = ['£',"££ - £££","££££"]

def city_scrape(_city,filename):


    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) '
                      'Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
    _city_split = _city.split('-')

    # overview

    try:
        request = urllib2.Request("https://www.tripadvisor.com/Tourism-"+_city+"-Vacations.html", headers=headers)
        print request
        soup = BeautifulSoup(urllib2.urlopen(request).read(), "html.parser")
    except:
        return
    try:
        entities = soup.find("div", {"class": "navLinks"}).find_all("li")  # find all overview type entities
    except:
        return
    cityname = str(soup.find("h1", {"id": "HEADING"}).text)
    overviews = {"city_name": cityname, "city_id": str(_city_split[0])}
    for overview in entities:
        try: _label = str(overview.find("span", {"class": "typeName"}).text).lower()
        except: pass
        try: _qty = int(str(overview.find("span", {"class": "typeQty"}).text.strip("()")).replace(',',''))
        except:_qty = -1
        if _label != "flights":
            try:
                _content = int(str(overview.find("span", {"class": "contentCount"}).text.split(' ', 1)[0]).replace(',',''))
            except:
                _content = -1
        else:
            try:
                _content = int(str(overview.find("span", {"class": "contentCount"}).text.replace(u'\xa0', u' ')).split(' ')[2].replace(',',''))
            except:
                _content = -1
        if (_label != "flights") and (_label != "forum"):
            overviews.update({_label+'_quantity': _qty})
            overviews.update({_label+'_content': _content})
        else:
            overviews.update({_label + '_content': _content})
    print overviews
    overviews_dataframe = pandas.DataFrame(data = overviews, index=["key"])

    writer = pandas.ExcelWriter(filename)
    overviews_dataframe.to_excel(writer, sheet_name="Overview")
    # hotels

    hotels = [[],[],[],[]]
    try:
        request = urllib2.Request("https://www.tripadvisor.co.uk/Hotels-"+_city+"-Hotels.html", headers=headers)
        soup = BeautifulSoup(urllib2.urlopen(request).read(), "html.parser")
    except:
        return
    while True:
        entities = soup.find_all("div", {"class": "listing easyClear  p13n_imperfect "})  # find all hotel entities
        for hotel in entities:
            _id = str(hotel["id"])
            try: _reviews = int(str(hotel.find("span", {"class": "more review_count"}).text).split(' ', 1)[0].replace(',',''))
            except:  _reviews = -1
            try: _rating = float(str(hotel.find("img", {"class": "sprite-ratings"})["alt"]).split(' ', 1)[0])
            except: _rating = -1.0
            _category = -1
            try:
                tags = hotel.find_all('a', {"class": "tag"})
                for tag in tags:
                    if str(tag.text) in HOTELTYPES:
                        _category = HOTELTYPES.index(str(tag.text))
            except:
                pass
            try:
                hotels[0].append(_id)
                hotels[1].append(_reviews)
                hotels[2].append(_rating)
                hotels[3].append(_category)
            except: pass

        nextpage = soup.find("a", {"class": "nav next ui_button primary taLnk"})
        if nextpage:
            _next = "https://www.tripadvisor.co.uk/"+str(nextpage["href"])
            request = urllib2.Request(_next, headers=headers)
            try:
                soup = BeautifulSoup(urllib2.urlopen(request).read(), "html.parser")
            except: break
        else:
            break

    print hotels
    hotels = numpy.array(hotels)
    hotels = {"name": hotels[0], "reviews": hotels[1], "ratings": hotels[2], "category": hotels[3]}
    hotels_dataframe = pandas.DataFrame(data = hotels)
    hotels_dataframe.to_excel(writer, sheet_name="Hotels")

    # attractions

    attractions = [[], [], []]
    try:
        request = urllib2.Request("https://www.tripadvisor.com/Attractions-"+_city_split[0]+"-Activities-"+_city_split[1]+
                                  ".html", headers=headers)
        soup = BeautifulSoup(urllib2.urlopen(request).read(), "html.parser")
    except:
        return
    while True:
        entities = soup.find_all("div", {"class": "entry"})   # find all attraction / activity type entities
        for activity in entities:
            try: _id = str(activity["id"])
            except: break
            try: _reviews = int(str(activity.find("span", {"class": "more"}).text).split(' ', 1)[0].replace("\n",'').replace(',',''))
            except: _reviews = -1
            try: _rating = float(str(activity.find("img", {"class": "sprite-ratings"})["alt"]).split(' ', 1)[0])
            except: _rating = -1.0
            try:
                attractions[0].append(_id)
                attractions[1].append(_reviews)
                attractions[2].append(_rating)
            except: pass

        nextpage = soup.find("a", {"class": "nav next rndBtn ui_button primary taLnk"})
        if nextpage:
            _next = "https://www.tripadvisor.com" +str(nextpage["href"])
            request = urllib2.Request(_next, headers=headers)
            soup = BeautifulSoup(urllib2.urlopen(request).read(), "html.parser")
        else:
            break

    print attractions
    attractions = numpy.array(attractions)
    attractions = {"name": attractions[0], "reviews": attractions[1], "ratings": attractions[2]}
    attractions_dataframe = pandas.DataFrame(data=attractions)
    attractions_dataframe.to_excel(writer, sheet_name="Attractions")
    # restaurants

    restaurants = [[],[],[],[]]
    try:
        request = urllib2.Request("https://www.tripadvisor.com/Restaurants-"+_city+".html", headers=headers)
        soup = BeautifulSoup(urllib2.urlopen(request).read(), "html.parser")
    except:
        return
    while True:
        entities = soup.find_all("div", class_="listing")
        for restaurant in entities:
            try: _id = str(restaurant["id"])
            except: break
            try:
                _reviews = int(str(restaurant.find("span", {"class": "reviewCount"}).text).split(' ', 1)[0].replace("\n",''))
            except: _reviews = -1
            try: _rating = float(str(restaurant.find("img", {"class": "sprite-ratings"})["alt"]).split(' ', 1)[0])
            except: _rating = -1.0
            _price = -1
            try:
                rangetag = str(restaurant.find("span", {"class", "price_range"}).text)
                if rangetag in PRICERANGE:
                    _price = PRICERANGE.index(rangetag)
            except:
                pass
            try:
                restaurants[0].append(_id)
                restaurants[1].append(_reviews)
                restaurants[2].append(_rating)
                restaurants[3].append(_price)
            except: pass

        nextpage = soup.find("a", {"class":"nav next rndBtn ui_button primary taLnk"})
        if nextpage:
            _next = "https://www.tripadvisor.com/"+str(nextpage["href"])
            request = urllib2.Request(_next, headers=headers)
            soup = BeautifulSoup(urllib2.urlopen(request).read(), "html.parser")
        else:
            break

    print restaurants
    restaurants = numpy.array(restaurants)
    restaurants = {"name": restaurants[0], "reviews": restaurants[1], "ratings": restaurants[2]}
    restaurants_dataframe = pandas.DataFrame(data=restaurants)
    restaurants_dataframe.to_excel(writer, sheet_name="Restaurants")

    writer.save()

    return


def get_city_list():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) '
                      'Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
    try:
        request = urllib2.Request("https://www.tripadvisor.co.uk", headers=headers)
        soup = BeautifulSoup(urllib2.urlopen(request).read(), "html.parser")
    except:
        return
    locations = []
    city_types = soup.find_all("div", {"class", "featured"})
    for category in city_types:
        city_type = category.find_all('a')
        for location in city_type:
            locations.append(str(location["href"]).replace("Hotels-",'').replace("-Hotels.html",''))
    return locations


def get_users_hotel(filename):
    city_overview = pandas.read_excel(filename+".xlsx", sheetname="Overview")   # open xlsx
    city_id = str(city_overview["city_id"][0])  # get link of hotel_id
    hotel_list = pandas.read_excel(filename+".xlsx", sheetname = "Hotels")["name"].base[0]
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) '
                      'Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
    city_users = []
    for hotel in hotel_list:
        hotel_link = str(hotel).split('_')[1]
        try:    # open hotel_id link
            request = urllib2.Request("https://www.tripadvisor.com/Hotel_Review-"+city_id+"-d"+hotel_link+"-Reviews.html", headers=headers)
            page = BeautifulSoup(urllib2.urlopen(request).read(), "html.parser")
        except:
            continue
        while True:
            reviews = page.find_all("div", {"class": "reviewSelector  "})
            for review in reviews:
                try:
                    city_users.append([hotel,str(review.find("div", {"class": "username mo"}).text).replace('\n','')])
                except:
                    continue
            #is next page in _id hotel?
            nextpage = page.find("a", {"class": "nav next rndBtn ui_button primary taLnk"})
            if nextpage:
                next_page = "https://www.tripadvisor.com" + str(nextpage["href"])
                request = urllib2.Request(next_page, headers=headers)
                try:
                    page = BeautifulSoup(urllib2.urlopen(request).read(), "html.parser")
                except:
                    break
            else:
                break
    print city_users
    city_users = numpy.array(city_users)
    city_users = {"hotel_id": city_users[0], "user": city_users[1]}
    city_users_dataframe = pandas.DataFrame(data=city_users)
    writer = pandas.ExcelWriter(filename+"_hotel_users.xlsx")
    city_users_dataframe.to_excel(writer)
    return



# city_scrape(link,link+".xlsx")

locations = get_city_list()
for city in locations:
    _filename = city.split('-')[0].replace('/','')
    city_scrape(city,_filename+".xlsx")
#get_users_hotel("g32655")



