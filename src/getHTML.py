import requests
from bs4 import BeautifulSoup


def getHTML(URL, headerInput):
    # Send an HTTP request to the URL/webpage to obtain the raw HTML data.
    with requests.Session() as s:
        r = s.get(URL, headers=headerInput)

    # Parse the raw HTML data from the URL/webpage request using Beautiful Soup.
    HTML = BeautifulSoup(r.content, "html.parser")
    return HTML
