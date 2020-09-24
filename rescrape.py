import configparser
import geopy
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import webbrowser
import requests
from bs4 import BeautifulSoup
import csv


# Read the input file.
config = configparser.ConfigParser()
config.read("res.inp")
StreetNumber = config.get("Address Control", "Street Number")
StreetName = config.get("Address Control", "Street Name")
AptNumber = config.get("Address Control", "Apartment Number")
City = config.get("Address Control", "City")
State = config.get("Address Control", "State")
ZipCode = config.get("Address Control", "Zip Code")
SearchBoxHalfWidth = config.getfloat("Search Control", "Search Box Half-Width (miles)")

# Construct the Address variable with the input supplied by the user
Address = (
    StreetNumber
    + " "
    + StreetName
    + " "
    + AptNumber
    + " "
    + City
    + " "
    + State
    + " "
    + ZipCode
)

# Nominatim is the GeoCoder class used in this code
geolocator = Nominatim(user_agent="my_app_rescrape")

# Using the GeoCoder, we obtain the coordinates of the user supplied address, and if the address cannot be found by
# the GeoCoder, we prompt the user for a new address. If the Address cannot be found, location
# is returned as None. When .latitude and .longitude are tried to be executed on a NoneType, the AttributeError is
# thrown and hence a new address from the user is prompted.
while True:
    try:
        location = geolocator.geocode(Address)
        origin = geopy.Point(location.latitude, location.longitude)
    except AttributeError:
        print(
            "ERROR!!! The user supplied address cannot be GeoCoded with Nominatim.\n"
            "In some instances, a mailing address is different from its physical address.\n"
            "If this is the case, please try supplying only the street number, name, state, and zip code."
        )
        Address = input(
            "Try typing in the specific physical address using method above: "
        )
        print("Trying to GeoCode the new address: ", Address)
    else:
        print("The address has been GeoCoded!")
        break
# The search box coordinates are obtained via a geodesic measurement from the origin (e.g. user supplied address) to the
# direct North, direct East, direct South, and direct West using the user supplied SearchBoxHalfWidth.
# The North Boundary thus becomes the latitude of the geodesic measurement from the origin, and so on.
NorthDestination = geodesic(kilometers=(SearchBoxHalfWidth * 1.60934)).destination(
    origin, 0.0
)
NorthBoundary = NorthDestination.latitude
EastDestination = geodesic(kilometers=(SearchBoxHalfWidth * 1.60934)).destination(
    origin, 90.0
)
EastBoundary = EastDestination.longitude
SouthDestination = geodesic(kilometers=(SearchBoxHalfWidth * 1.60934)).destination(
    origin, 180.0
)
SouthBoundary = SouthDestination.latitude
WestDestination = geodesic(kilometers=(SearchBoxHalfWidth * 1.60934)).destination(
    origin, 270.0
)
WestBoundary = WestDestination.longitude
print("Searching within a square area of half-width", SearchBoxHalfWidth, "miles.")

# Construct the Zillow Recently Sold Homes URL using the search boundary found above.
ZillowURL = [
    "https://www.zillow.com/homes/recently_sold/?searchQueryState={"
    '"pagination":{},'
    '"mapBounds":{'
    '"west":'
    + str(WestBoundary)
    + ',"east":'
    + str(EastBoundary)
    + ',"south":'
    + str(SouthBoundary)
    + ',"north":'
    + str(NorthBoundary)
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

# The headers for the HTTP request below comes from inspecting the zillow url's html code:
# https://stackoverflow.com/questions/46623658/whats-the-best-way-to-scrape-data-from-zillow.
req_headers = {
    "accept": "/",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/85.0.4183.102 "
                  "Safari/537.36",
}

# Send an HTTP request to the Zillow URL to obtain the raw HTML data.
with requests.Session() as s:
    r = s.get(ZillowURL[0], headers=req_headers)

# Parse the raw HTML data from the Zillow URL request using Beautiful Soup.
ZillowHTML = BeautifulSoup(r.content, "html.parser")

# Find the number of pages associated with the Zillow search.
ZillowPageList = ZillowHTML.find("div", class_="search-pagination")
if ZillowPageList is None:
    print("Only 1 page of Zillow search results exist in this search box.")
    NumZillowPages = 1
else:
    ZillowPageLinks = ZillowPageList.find_all("a")
    print(
        ZillowPageLinks[-2].text,
        "pages of Zillow search results exist in this search box.",
    )
    NumZillowPages = int(ZillowPageLinks[-2].text)

# Find the total number of Zillow results, and store as an integer.
ZillowResultCount = int(
    (ZillowHTML.find("span", class_="result-count")).text.split()[0].replace(",", "")
)
print(
    ZillowResultCount, "recently sold homes on Zillow were found within the search box."
)

# Zillow limits the number of pages of a search to 20, and the number of results/page to 40; therefore, the maximum
# number of results one can obtain is 800.
if ZillowResultCount > 800:
    print(
        "Warning! The maximum number of pages Zillow shows is 20 and the maximum number of results per page is 40. \n"
        "Therefore, only 800 recently sold home links will be scraped."
    )
    ZillowResultCount = 800

# Loop over the number of pages found from the original zillow search to obtain each
# recently sold home link from each page.
SoldHomeZillowLinks = []
for i in range(0, NumZillowPages):

    if i == 0:

        # The page one URL was already requested and parsed above; therefore, we scrape it to
        # get all of the sold homes' URL link info.
        SoldHomeZillowLinkInfo = ZillowHTML.find_all("div", class_="list-card-info")

        # Zillow automatically recommends additional "relaxed search results" that populate in its page
        # when not many results were returned due to restrictive search criteria (e.g. search area too small).
        # Therefore, we exclude Zillow's "relaxed search results" from the sold home links that we actually store by
        # looping over the number of Zillow Results found just from the search (ZillowResultCount) or 40, whichever
        # is smaller since the page is limited to 40 results.
        for j in range(0, min(ZillowResultCount, 40)):
            # For each sold home URL, store the href value (which is that actual URL link itself).
            SoldHomeZillowLinks.append(
                SoldHomeZillowLinkInfo[j].find("a", class_="list-card-link")["href"]
            )
    else:
        # For each page after page one, the Zillow URL must be constructed, requested, parsed, and scraped.
        # Construct each Zillow URL associated with each subsequent page.
        ZillowURL.append(
            "https://www.zillow.com/homes/recently_sold/"
            + str(i + 1)
            + "_p/?searchQueryState={"
            '"pagination":{"currentPage":' + str(i + 1) + "},"
            '"mapBounds":{'
            '"west":'
            + str(WestBoundary)
            + ',"east":'
            + str(EastBoundary)
            + ',"south":'
            + str(SouthBoundary)
            + ',"north":'
            + str(NorthBoundary)
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
        )

        # Send an HTTP request to the Zillow URL to obtain the raw HTML data, using the same headers defined above.
        with requests.Session() as s:
            r = s.get(ZillowURL[i], headers=req_headers)

        # Parse the raw HTML data from the Zillow URL request using Beautiful Soup.
        ZillowHTML = BeautifulSoup(r.content, "html.parser")

        # Scrape the current Zillow page to obtain all of the sold homes' URL link info.
        SoldHomeZillowLinkInfo = ZillowHTML.find_all("div", class_="list-card-info")

        # For each sold home URL, store the href value (actual URL link).
        for Link in SoldHomeZillowLinkInfo:
            SoldHomeZillowLinks.append(Link.find("a", class_="list-card-link")["href"])

# All Sold Home Zillow URLs from the user's search box are printed to screen, in case the user needs to quickly visit
# any one of them.
print(*SoldHomeZillowLinks, sep="\n")

# An equality check is completed to make sure the number of SoldHomeZillowLinks is the same as the ZillowResultCount.
# The number of SoldHomeZillowLinks is a count of each link we scraped. The ZillowResultCount is the total number of
# search results from the original Zillow search web page. If they are not equal, it may mean more or less sold home
# URLs have been scraped than what the original Zillow search result count was from the original Zillow web page.
if len(SoldHomeZillowLinks) == ZillowResultCount:
    print(
        "The number of Sold Home Zillow Links scraped from all pages equals \n"
        "the Zillow Result Count that was scraped from the initial page."
    )
else:
    print(
        "WARNING!!! The number of Sold Home Zillow Links scraped from all pages DOES NOT EQUAL \n"
        "the Zillow Result Count that was scraped from the initial page. There may be an issue with Zillow \n"
        "recommending/providing additional links on subsequent pages that weren't originally included in \n"
        "the Zillow Result Count."
    )

# Loop over each recently sold home Zillow URL and scrape pertinent sold home details and information, and print the
# results to the screen.
print(
    "{:^55s}{:^10s}{:>10s}{:>6s}{:^17s}{:^7s}{:^22s}{:^9s}{:^17s}{:^12s}".format(
        "Address",
        "Sell Price",
        "Bed/Bath",
        "SqFt",
        "Type",
        "Built",
        "Heating",
        "Cooling",
        "Parking",
        "Lot Size",
    )
)

for i in range(0, len(SoldHomeZillowLinks)):

    # Send an HTTP request to the Zillow URL to obtain the raw HTML data, using the same headers defined above.
    with requests.Session() as s:
        r = s.get(SoldHomeZillowLinks[i], headers=req_headers)
    # Parse the raw HTML data from the Zillow URL request using Beautiful Soup.
    ZillowHTML = BeautifulSoup(r.content, "html.parser")

    # Scrape the current Zillow page to obtain the sold homes' details and information (e.g. address, price, size, etc).
    # The sold home address is simply taken directly from its own URL.
    SoldHomeAddress = (
        SoldHomeZillowLinks[i]
        .replace("https://www.zillow.com/homedetails/", "")
        .replace("-", " ")
        .split("/", 1)[0]
    )

    # We try to find the SoldHomePrice using a try-except statement because in some cases the HTML tag/class we are
    # searching for does not exist, which means the ZillowHTML.find() will return None, and the subsequent .find()
    # on a NoneType throws an AttributeError. When this AttributeError is thrown, we store "n/a" into the SoldHomePrice
    # variable.
    # Currently, this scraper cannot scrape information from Zillow web pages that use Java Script to subsequently load
    # webpage details. Java Script transactions on a webpage delay the download of information (i.e. details are not
    # shown until user clicks an "expand" button) which results in the HTTP request not obtaining a "full" response from
    # the server. Selenium WebDriver could be used as a solution to query these JS pages in order to fully acquire all
    # information on a web page.
    try:
        SoldHomePrice = (
            ZillowHTML.find("div", class_="ds-home-details-chip")
            .find("p")
            .text.split()[1]
            .replace("$", "")
            .replace(",", "")
            .replace("Sold", "")
        )
    except AttributeError:
        SoldHomePrice = "n/a"
    # Next, we search for the number of beds, baths, and the home's square footage. These items are scraped and stored
    # in Home_Size_items using a try-except statement for the same reasons discussed above. In this case, when an
    # AttributeError is thrown, we store an empty list into Home_Size_items, which will cause the subsequent try-except
    # statements to throw an IndexError, which will ultimately cause "n/a" to be stored for the number of beds, baths,
    # and/or sqft.
    try:
        Home_Size_container = ZillowHTML.find(
            "h3", class_="ds-bed-bath-living-area-container"
        )
        Home_Size_items = []
        for item in Home_Size_container.select(
            ".ds-bed-bath-living-area span:not(.ds-vertical-divider)"
        ):
            Home_Size_items.append(item.text)
    except AttributeError:
        Home_Size_items = []
    # Now, for each item in Home_Size_items, we look for the words "bd", "ba", and "Square Feet", which is what Zillow
    # uses to label number of beds, baths, and square footage. If we find these key words, we obtain that element's
    # position in the list (i.e. its index). We know that the element in front of each key word is the actual value.
    # For example, if "bd" is found in the Home_Size_items list, and it's index = 2, then we know the actual value for
    # the number of beds is contained in the Home_Size_items list at index 1. The associated value is then stored in the
    # appropriate variable. The try-except statement is used so that if "bd", "ba", or "Square Feet" is not found
    # (i.e. possibly because the web page we are currently scraping is actually for a recently sold parcel of land that
    # only obviously shows the square footage), an IndexError is thrown, and "n/a" is stored instead. Or, if
    # Home_Size_items is an empty list (see above), an IndexError will also be thrown, and "n/a" will be stored.
    try:
        index = [j for j, x in enumerate(Home_Size_items) if "bd" in x.lower()]
        SoldHomeBeds = Home_Size_items[index[0] - 1]
    except IndexError:
        SoldHomeBeds = "n/a"
    try:
        index = [j for j, x in enumerate(Home_Size_items) if "ba" in x.lower()]
        SoldHomeBaths = Home_Size_items[index[0] - 1]
    except IndexError:
        SoldHomeBaths = "n/a"
    try:
        index = [j for j, x in enumerate(Home_Size_items) if "square feet" in x.lower()]
        SoldHomeSqFt = Home_Size_items[index[0] - 1]
    except IndexError:
        SoldHomeSqFt = "n/a"
    # Next, we search for the home type, year built, heating, cooling, parking, and lot size details of the house.
    # These details, or "facts" as Zillow calls them, are contained within a fact-label class and a fact-value class.
    # The labels and values are stored accordingly using a try-except statement because in some cases the information
    # cannot be found and thus a "n/a" needs to be stored instead (e.g. the web page we are scraping is of a recently
    # sold parcel of land with no actual home on it, so information like "year built" does not exist). If the labels and
    # values cannot be found, the ZillowHTML.find() will return None, and the .find_all() on a NoneType throws an
    # AttributeError. When this AttributeError is thrown, "n/a" is stored into the type, year built, heating, cooling,
    # parking, and lot size variables.
    # 9/20/2020 - updated classes in below .find() statements to account for new zillow layout
    try:
        SoldHomeFactLabels = ZillowHTML.find("ul", class_="ds-home-fact-list").find_all(
            "span", class_="ds-home-fact-label"
        )
        SoldHomeFactValues = ZillowHTML.find("ul", class_="ds-home-fact-list").find_all(
            "span", class_="ds-home-fact-value"
        )
    except AttributeError:
        SoldHomeType = "n/a"
        SoldHomeYearBuilt = "n/a"
        SoldHomeHeating = "n/a"
        SoldHomeCooling = "n/a"
        SoldHomeParking = "n/a"
        SoldHomeLotSize = "n/a"
    # If there is information in SoldHomeFactLabels and SoldHomeFactValues, such that the above error is not
    # thrown, the following else statement is executed.
    else:
        # Within SoldHomeFactLabels, we try to find each specific label's index (e.g. what position is the "year built"
        # label inside SoldHomeFactLabels). Subsequently, using that index, we know the label's corresponding value
        # (e.g. 1969) has the same index but is obviously located in SoldHomeFactValues. So if the index of "year built"
        # in SoldHomeFactLabels is 2, we know that the index of its corresponding value, 1969, in SoldHomeFactValues is
        # also 2. The values of these labels are thus stored into the appropriate variables. If we cannot find the
        # specific label within SoldHomeFactLabels, the index variable becomes an empty list, and when that empty list
        # is referenced in the following statement for storing the actual value, an IndexError will be thrown and "n/a"
        # will be stored instead.
        try:
            index = [
                j for j, x in enumerate(SoldHomeFactLabels) if "type" in x.text.lower()
            ]
            SoldHomeType = SoldHomeFactValues[index[0]].text
        except IndexError:
            SoldHomeType = "n/a"
        try:
            index = [
                j
                for j, x in enumerate(SoldHomeFactLabels)
                if "year built" in x.text.lower()
            ]
            SoldHomeYearBuilt = SoldHomeFactValues[index[0]].text
        except IndexError:
            SoldHomeYearBuilt = "n/a"
        try:
            index = [
                j
                for j, x in enumerate(SoldHomeFactLabels)
                if "heating" in x.text.lower()
            ]
            SoldHomeHeating = SoldHomeFactValues[index[0]].text
        except IndexError:
            SoldHomeHeating = "n/a"
        try:
            index = [
                j
                for j, x in enumerate(SoldHomeFactLabels)
                if "cooling" in x.text.lower()
            ]
            SoldHomeCooling = SoldHomeFactValues[index[0]].text
        except IndexError:
            SoldHomeCooling = "n/a"
        try:
            index = [
                j
                for j, x in enumerate(SoldHomeFactLabels)
                if "parking" in x.text.lower()
            ]
            SoldHomeParking = SoldHomeFactValues[index[0]].text
        except IndexError:
            SoldHomeParking = "n/a"
        try:
            index = [
                j for j, x in enumerate(SoldHomeFactLabels) if "lot" in x.text.lower()
            ]
            SoldHomeLotSize = SoldHomeFactValues[index[0]].text
        except IndexError:
            SoldHomeLotSize = "n/a"
    # Print the results of the scraping to the screen
    print(
        "{:55s}{:>2s}{:>8s}{:>4s}{:^3s}{:3s}{:>6s}"
        "{:^17}{:^7}{:^22}{:^9}{:^17}{:^12}".format(
            SoldHomeAddress,
            "$",
            SoldHomePrice,
            SoldHomeBeds,
            "/",
            SoldHomeBaths,
            SoldHomeSqFt,
            SoldHomeType,
            SoldHomeYearBuilt,
            SoldHomeHeating,
            SoldHomeCooling,
            SoldHomeParking,
            SoldHomeLotSize,
        )
    )
