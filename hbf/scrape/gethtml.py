import requests
from bs4 import BeautifulSoup


def gethtml(url, header_input):
    # Send an HTTP request to the URL/webpage to obtain the raw html data.
    with requests.Session() as s:
        r = s.get(url, headers=header_input)

    # Parse the raw html data from the URL/webpage request using Beautiful Soup.
    html = BeautifulSoup(r.content, "html.parser")
    return html
