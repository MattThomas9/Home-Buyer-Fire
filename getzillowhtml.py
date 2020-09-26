import requests
from bs4 import BeautifulSoup

def getZillowHTML(pagetype, pagenumber, urlvariables, reqdheaders):
    if pagetype == "Recently Sold":
        if len(urlvariables) != 4:
            print(
                "ERROR!!! getZillowHTML.py requires 4 boundaries to be passed in a list as the second argument \n"
                " when constructing a 'Recently Sold' page. \n"
                "Zillow Page was not constructed"
            )
            return
        elif "north" not in [x[0].lower() for j, x in enumerate(urlvariables)] or \
             "south" not in [x[0].lower() for j, x in enumerate(urlvariables)] or \
             "east" not in [x[0].lower() for j, x in enumerate(urlvariables)] or \
             "west" not in [x[0].lower() for j, x in enumerate(urlvariables)]:
            print("ERROR!!! getzillowHTML.py requires 'north', 'south', 'east', and 'west' identifiers \n"
                  "to be placed in the second argument list as tuples with the value or variable they qualify ")
            return
        else:
            if pagenumber is None:
                # Construct the Zillow Recently Sold Homes URL (first/initial page) using the search boundary.
                zillowurl = [
                    "https://www.zillow.com/homes/recently_sold/?searchQueryState={"
                    '"pagination":{},'
                    '"mapBounds":{'
                    '"west":'
                    + str([x for j, x in enumerate(urlvariables) if "west" in x[0].lower()][0][1])
                    + ',"east":'
                    + str([x for j, x in enumerate(urlvariables) if "east" in x[0].lower()][0][1])
                    + ',"south":'
                    + str([x for j, x in enumerate(urlvariables) if "south" in x[0].lower()][0][1])
                    + ',"north":'
                    + str([x for j, x in enumerate(urlvariables) if "north" in x[0].lower()][0][1])
                    + "},"
                      '"isMapVisible":true,'
                      '"mapZoom":8,'
                      '"filterState":{'
                      '"isForSaleByAgent":{"value":false},'
                      '"isForSaleByOwner":{"value":false},'
                      '"isNewConstruction":{"value":false},'
                      '"isForSaleForeclosure":{"value":false},'
                      '"isComingSoon":{"value":false},'
                      '"isAuction":{"value":false},'
                      '"isPreMarketForeclosure":{"value":false},'
                      '"isPreMarketPreForeclosure":{"value":false},'
                      '"isMakeMeMove":{"value":false},'
                      '"isRecentlySold":{"value":true}},'
                      '"isListVisible":true}'
                ]
            else:
                # Construct the Zillow Recently Sold Homes URL (subsequent pages) using the search boundary.
                zillowurl = [
                    "https://www.zillow.com/homes/recently_sold/"
                    + str(pagenumber + 1)
                    + "_p/?searchQueryState={"
                    '"pagination":{"currentPage":' + str(pagenumber + 1) + "},"
                    '"mapBounds":{'
                    '"west":'
                    + str([x for j, x in enumerate(urlvariables) if "west" in x[0].lower()][0][1])
                    + ',"east":'
                    + str([x for j, x in enumerate(urlvariables) if "east" in x[0].lower()][0][1])
                    + ',"south":'
                    + str([x for j, x in enumerate(urlvariables) if "south" in x[0].lower()][0][1])
                    + ',"north":'
                    + str([x for j, x in enumerate(urlvariables) if "north" in x[0].lower()][0][1])
                    + "},"
                    '"isMapVisible":true,'
                    '"mapZoom":15,'
                    '"filterState":{'
                    '"isForSaleByAgent":{"value":false},'
                    '"isForSaleByOwner":{"value":false},'
                    '"isNewConstruction":{"value":false},'
                    '"isForSaleForeclosure":{"value":false},'
                    '"isComingSoon":{"value":false},'
                    '"isAuction":{"value":false},'
                    '"isPreMarketForeclosure":{"value":false},'
                    '"isPreMarketPreForeclosure":{"value":false},'
                    '"isMakeMeMove":{"value":false},'
                    '"isRecentlySold":{"value":true}},'
                    '"isListVisible":true}'
                ]

            # Send an HTTP request to the Zillow URL to obtain the raw HTML data.
            with requests.Session() as s:
                r = s.get(zillowurl[0], headers=reqdheaders)

            # Parse the raw HTML data from the Zillow URL request using Beautiful Soup.
            zillowhtml = BeautifulSoup(r.content, "html.parser")
            return zillowhtml, zillowurl
