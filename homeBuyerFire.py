import sys
from getAddress import getAddress
from getBox import getBox
from getURLs import getURLs
from scrapeZillowLinks import scrapeZillowLinks
from soldHomeDF import soldHomeDF

# Step 1: Build address and obtain search box half width from command-line input file.
Address, SearchBoxHalfWidth = getAddress(sys.argv[1])

# Step 2: Get search box coordinates.
NorthBoundary, EastBoundary, SouthBoundary, WestBoundary = getBox(
    Address, SearchBoxHalfWidth
)

# The headers for the HTTP request below comes from inspecting the zillow url's html code:
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

# Step 3: Get all sold home Zillow URLs from the user's search box.
SoldHomeZillowLinks = getURLs(
                        NorthBoundary,
                        EastBoundary,
                        SouthBoundary,
                        WestBoundary,
                        req_headers
                      )

# Step 4: Create a list containing all sold home data scraped from Zillow URLs.
SoldHomeDataList = scrapeZillowLinks(SoldHomeZillowLinks, req_headers)

# Step 5: Construct pandas dataframe from SoldHomeDataList.
SoldHomeData = soldHomeDF(SoldHomeDataList)
