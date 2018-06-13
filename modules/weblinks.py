import re
import requests
import tldextract

from modules import pagereader
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError, HTTPError
from geopy.geocoders import Nominatim

def valid_url(url, extensions=False):
    """Checks for any valid url using regular expression matching
        Matches all possible url patterns with the url that is passed and
        returns True if it is a url and returns False if it is not.
        Args:
            url: string representing url to be checked
        Returns:
            bool: True if valid url format and False if not
    """
    pattern = r"^https?:\/\/(www\.)?([a-z,A-Z,0-9]*)\.([a-z, A-Z]+)(.*)"
    regex = re.compile(pattern)
    if not extensions:
        if regex.match(url):
            return True
        return False

    parts = tldextract.extract(url)
    valid_sites = list()
    for ext in extensions:
        if regex.match(url) and '.' + parts.suffix in ext:
            valid_sites.append(url)
    return valid_sites


def get_address(soup, ext=False, live=False):
    """
        Searches through all <a ref> (hyperlinks) tags and stores them in a
        list then validates if the url is formatted correctly.
        Args:
            soup: BeautifulSoup instance currently being used.
        Returns:
            websites: List of websites that were found
    """

    if isinstance(soup, BeautifulSoup):
        client = []
        geolocator = Nominatim()
        for item in soup.find_all("div", {"class": "result-box -hover-trigger clearfix"}):
            address = item.find("div", {"class": "result-address"})
            cliente_name = item.find("span", {"class": "result-bn medium"}).get_text()
            print(address.get_text("\n"))
            try:
                valid_address = address.get_text("\n").split("\n")
                location = geolocator.geocode(valid_address[0] + " Porto")
                client.append({'cliente': cliente_name, 'latitude': location.latitude, 'longitude': location.longitude})
                if location is None:
                    raise ValueError("None location found, please verify your address line")
            except:
                print("Invalid Address")

        return client

    else:
        raise (Exception('Method parameter is not of instance BeautifulSoup'))


def print_row(url, description):
    print("%-80s %-30s" % (url, description))