import requests

from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError, HTTPError, MissingSchema
from sys import exit


def connection_msg(site):
    yield "Attempting to connect to {site}".format(site=site)


def read_first_page(site, extension=False):
    headers = ''
    attempts_left = 3
    err = " "
    while attempts_left:
        try:
            if not extension:
                print(next(connection_msg(site)))
                response = requests.get(site, headers=headers)
                print("Connection successful.")
                page = BeautifulSoup(response.text, 'html.parser')
                return page
            if extension and attempts_left == 3:
                print(next(connection_msg('https://'+site)))
                response = requests.get('https://'+site, headers=headers)
                print("Connection successful.")
                page = BeautifulSoup(response.text, 'html.parser')
                return page
            if extension and attempts_left == 2:
                print(next(connection_msg('http://'+site)))
                response = requests.get('http://'+site, headers=headers)
                print("Connection successful.")
                page = BeautifulSoup(response.text, 'html.parser')
                return page
            if extension and attempts_left == 1:
                msg = ''.join(("There has been an {err} while attempting to ",
                              "connect to {site}.")).format(err=err, site=site)
                exit(msg)

        except (HTTPError, ConnectionError) as e:
            attempts_left -= 1
            err = e

    if err == HTTPError:
        raise("There has been an HTTP error after three attempts.")
    if err == ConnectionError:
        raise("There has been a connection error after three attempts.")


def read_page(site):
    headers = ''
    attempts_left = 3
    err = " "
    while attempts_left:
        try:
            if attempts_left == 3:
                response = requests.get(site, headers=headers)
                page = BeautifulSoup(response.text, 'html.parser')
                return page
            if attempts_left == 2:
                response = requests.get('https://'+site, headers=headers)
                page = BeautifulSoup(response.text, 'html.parser')
                return page
            if attempts_left == 1:
                response = requests.get('http://'+site, headers=headers)
                page = BeautifulSoup(response.text, 'html.parser')
                return page
            if not attempts_left:
                msg = ''.join(("There has been an {err} while attempting to ",
                              "connect to {site}.")).format(err=err, site=site)
                exit(msg)

        except (HTTPError, MissingSchema, ConnectionError) as e:
            attempts_left -= 1
            err = e

    if isinstance(err, HTTPError):
        print("There has been an HTTP error after three attempts.")
        exit (1)
    if isinstance(err, ConnectionError):
        print("There has been a connection error after three attempts.")
        exit (1)

