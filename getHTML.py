import requests
from getZillowRequestHeaders import getZillowRequestHeaders
from bs4 import BeautifulSoup


def getHTML(URL):
    # Send an HTTP request to the URL/webpage to obtain the raw HTML data.
    with requests.Session() as s:
        r = s.get(URL, headers=getZillowRequestHeaders())

    # Parse the raw HTML data from the URL/webpage request using Beautiful Soup.
    HTML = BeautifulSoup(r.content, "html.parser")
    return HTML
