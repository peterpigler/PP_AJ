from bs4 import BeautifulSoup
import urllib2
# import pandas


def tripadvisor_city():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) '
                      'Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

    link = "g274919-Veszprem_Veszprem_County_Central_Transdanubia"

    # overview

    try:
        request = urllib2.Request("https://www.tripadvisor.com/Tourism-"+link+"-Vacations.html", headers=headers)
        soup = BeautifulSoup(urllib2.urlopen(request).read(), "html.parser")
    except:
        return
    typenames = soup.find("div", {"class": "navLinks"}).find_all("li")  # find all overview type entities

    overviews = {}
    for overview in typenames:
        try: _label = overview.find("span", {"class": "typeName"}).text
        except: break
        try: _qty = overview.find("span", {"class": "typeQty"}).text.strip("()")
        except:_qty = 0.0
        try: _content = overview.find("span", {"class": "contentCount"}).text.split(' ', 1)[0]
        except: _content = 0.0
        try:
            overviews.update({_label : float(_qty)})
            try: overviews.update({_label+"_content": float(_content)})
            except: pass
        except:
            try: overviews.update({_label: float(_content)})
            except: pass

    print overviews


    # hotels

    try:
        request = urllib2.Request("https://www.tripadvisor.com/Hotels-"+link+"-Hotels.html", headers=headers)
        soup = BeautifulSoup(urllib2.urlopen(request).read(), "html.parser")
    except:
        return
    typenames = soup.find_all("div", {"class": "listing easyClear  p13n_imperfect "})  # find all hotel type entities
    hotels = []
    for hotel in typenames:
        try: _name = hotel.find("div", {"class": "listing_title"}).text
        except: break
        try: _reviews = hotel.find("span", {"class": "more review_count"}).text.split(' ', 1)[0]
        except:  _reviews = 0.0
        try: _rating = hotel.find("img", {"class": "sprite-ratings"})["alt"].split(' ', 1)[0]
        except: _rating = 0.0
        try:
            hotels.append({"name": _name})
            hotels.append({"reviews": int(_reviews)})
            hotels.append({"ranking": float(_rating)})
        except: pass

    print hotels


    # attractions

    try:
        request = urllib2.Request("https://www.tripadvisor.com/Attractions-g274919-Activities-Veszprem_Veszprem_County_Central_Transdanubia.html", headers=headers)
        soup = BeautifulSoup(urllib2.urlopen(request).read(), "html.parser")
    except:
        return
    typenames = soup.find_all("div", {"class": "entry"})   # find all attraction / activity type entities
    attractions = []
    for activity in typenames:
        try: _name = activity.find("div", {"class": "property_title"}).text.strip("\n")
        except: break
        try: _reviews = activity.find("span", {"class": "more"}).text.split(' ', 1)[0]
        except: _reviews = 0.0
        try: _rating = activity.find("img", {"class": "sprite-ratings"})["alt"].split(' ', 1)[0]
        except: _rating = 0.0
        try:
            attractions.append({"name": _name})
            attractions.append({"reviews": int(_reviews)})
            attractions.append({"rating": float(_rating)})
        except: pass

    print attractions


    # restaurants

    try:
        request = urllib2.Request("https://www.tripadvisor.com/Restaurants-"+link+".html", headers=headers)
        soup = BeautifulSoup(urllib2.urlopen(request).read(), "html.parser")
    except:
        return
    typenames = soup.find_all("div", {"class": "listing"})
    restaurants = []

    for restaurant in typenames:
        try:_name = restaurant.find("h3", {"class": "title"}).text.strip("\n")
        except: break
        try:
            _reviews = restaurant.find("span", {"class": "reviewCount"}).text.split(' ', 1)[0]
        except: _reviews = 0.0
        try: _rating = restaurant.find("img", {"class": "sprite-ratings"})["alt"].split(' ', 1)[0]
        except: _rating = 0.0
        try:
            restaurants.append({"name": _name})
            restaurants.append({"reviews": int(_reviews)})
            restaurants.append({"rating": float(_rating)})
        except: pass
    print restaurants

    return


tripadvisor_city()
