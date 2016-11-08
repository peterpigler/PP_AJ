# coding=utf-8
# encoding=utf-8
import urllib2
from bs4 import BeautifulSoup
"""
@lib: Soup

@author: Peter Pigler
"""
headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) '
                      'Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}


TRIPADVISORCOM = "https://www.tripadvisor.com"
TRIPADVISORUK = "https://www.tripadvisor.co.uk"
TRIPADVISORHU = "https://www.tripadvisor.co.hu"

def open(link):
    """
        Parameters
        ----
        link: String
            Desired link to be parsed into BSObj.

        Description
        ----
        Returns a BSObj with urllib2 method, using the html parser, Headers and Tripadvisor localization prefixes.

        Returns
        -----
        s:  BSObject
        """
    request = urllib2.Request(link, headers=headers)
    soup = BeautifulSoup(urllib2.urlopen(request).read(), "html.parser")
    return soup