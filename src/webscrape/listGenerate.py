"""
@lib: listGenerate

@author: Peter Pigler
"""
import soup as soupOpen


def getLocalizationCityList(link):
    """
        Parameters
        ----
        link: String
            Desired soupOpen link to be parsed into BSObj.

        Description
        ----
        Returns a python-list of links with urllib2 method, using the html parser, Headers and Tripadvisor
        localization prefixes found
        in the soup lib.

        Returns
        -----
        l: python_list
        """
    try:
        soup = soupOpen.open(link)
    except:
        return
    result = {"city_name": [], "city_id":[]}
    city_types = soup.find_all("div", {"class", "featured"})
    for category in city_types:
        city_type = category.find_all('a')
        for location in city_type:
            result["city_id"].append(str(location["href"]).strip('-')[1])
            result["city_name"].append(str(location["href"]).strip('-')[2])
    return result


def getCityList(countryID): # returns list cities within given countryID's from
    """
       Parameters
       ----
       countryID: String
           Desired Tripadvisor country_id

       Description
       ----
       Returns a python-list of links using link generate under Tripadvisor hood with urllib2 method, using the
       html parser, Headers and Tripadvisor localization prefixes found in the soup lib.

       Returns
       -----
       l: python_list
           """
    result = {"city_name": [], "city_id":[]}
    try:
        soup = soupOpen.open(soupOpen.TRIPADVISORUK+"/Hotels-"+countryID)
    except:
        return
    while True:
        cities_on_page = soup.find_all("div", {"class": "geo_name"})
        for city in cities_on_page:
            result["city_id"].append(str(city.find('a')["href"]).split('-')[1])
            result["city_name"].append(str(city.find('a').text).split(' ')[0])
        nextpage = soup.find('a', {"class": "nav next ui_button primary taLnk"})
        if nextpage:
            _next = soupOpen.TRIPADVISORUK+str(nextpage["href"])
            soup = soupOpen.open(_next)
        else:
            nextpage = soup.find('a', {"class": "nav next rndBtn ui_button primary taLnk"})
            if nextpage:
                _next = soupOpen.TRIPADVISORUK + str(nextpage["href"])
                soup = soupOpen.open(_next)
            else:
                break
    return result


def getAccentsensitiveList():
    """
       Description
       ----
       Returns a python-list of accent city names and links using link generate under Tripadvisor hood with
       urllib2 method, using the html parser, Headers and Tripadvisor localization prefixes found in the soup lib.

       Returns
       -----
       l: python_list
           """
    result = {"city_name": [], "city_id":[]}
    try:
        soup = soupOpen.open(soupOpen.TRIPADVISORHU+"/Hotels-g274881-Hungary-Hotels.html#LOCATION_LIST")
    except:
        return
    while True:
        cities_on_page = soup.find_all("div", {"class": "geo_name"})
        for city in cities_on_page:
            result["city_name"].append(str(city.find('a').text).split(' ')[0])
            result["city_id"].append(str(city.find('a')["href"]).split('-')[1])
        nextpage = soup.find('a', {"class": "nav next ui_button primary taLnk"})
        if nextpage:
            _next = soupOpen.TRIPADVISORHU + str(nextpage["href"])
            soup = soupOpen.open(_next)
        else:
            nextpage = soup.find('a', {"class": "nav next rndBtn ui_button primary taLnk"})
            if nextpage:
                _next = soupOpen.TRIPADVISORHU + str(nextpage["href"])
                soup = soupOpen.open(_next)
            else:
                break
    return result

def findCityList(country):
    """
           Parameters
           ----
           countryID: String
               Desired Tripadvisor country_id

           Description
           ----
           Returns a python-list of links using link generate under Tripadvisor hood with dynamic search urllib2 method,
            using the html parser, Headers and Tripadvisor localization prefixes found in the soup lib.

           Returns
           -----
           l: python_list
               """

    soup = soupOpen.open("https://www.tripadvisor.com/ForumHome")
    result = []
    id = ''
    continents_on_page = soup.find_all("td", {"class", "pb5"}, limit = 11)
    for continent in continents_on_page:
        forum = soupOpen.open(soupOpen.TRIPADVISORCOM+continent.find('a')["href"])
        forum_country = forum.find_all("td", {"class": "fname"})
        for city in forum_country:
            if str(city.text).replace('\n','') == country:
                print city.text
                id = city.find('a')["href"].split('-')[1]
                break
    if id != '':
        result = getCityList(id)
    return result