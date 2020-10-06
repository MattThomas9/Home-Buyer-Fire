import sys
from getInput import getInput
from getAddress import getAddress
from getBox import getBox
from getAllSoldHomeZillowURLs import getAllSoldHomeZillowURLs
from scrapeZillowLinks import scrapeZillowLinks
from soldHomeDF import soldHomeDF

# Step 0: Get input parameters from file.
StreetNumber, StreetName, AptNumber, City, State, ZipCode, SearchBoxHalfWidth, RequestHeaders = getInput(sys.argv[1])

# Step 1: Build address and obtain search box half width from command-line input file.
Address = getAddress(StreetNumber,
                     StreetName,
                     AptNumber,
                     City,
                     State,
                     ZipCode
                    )

# Step 2: Get search box coordinates.
NorthBoundary, SouthBoundary, EastBoundary, WestBoundary = getBox(
    Address, SearchBoxHalfWidth
)

# Step 3: Get all sold home Zillow URLs from the user's search box.
SoldHomeZillowLinks = getAllSoldHomeZillowURLs(
                        NorthBoundary,
                        SouthBoundary,
                        EastBoundary,
                        WestBoundary,
                        RequestHeaders
                      )

# Step 4: Create a list containing all sold home data scraped from Zillow URLs.
SoldHomeDataList = scrapeZillowLinks(SoldHomeZillowLinks, RequestHeaders)

# Step 5: Construct pandas dataframe from SoldHomeDataList.
SoldHomeData = soldHomeDF(SoldHomeDataList)
