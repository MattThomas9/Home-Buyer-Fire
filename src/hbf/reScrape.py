import sys
from src.hbf.getInput import getInput
from src.hbf.getAddress import getAddress
from src.hbf.getBox import getBox
from src.hbf.getAllSoldHomeZillowURLs import getAllSoldHomeZillowURLs
from src.hbf.scrapeZillowLinks import scrapeZillowLinks
from src.hbf.soldHomeDF import soldHomeDF

# Step 0: Get input parameters from file.
(
    StreetNumber,
    StreetName,
    AptNumber,
    City,
    State,
    ZipCode,
    SearchBoxHalfWidth,
    RequestHeaders,
) = getInput(sys.argv[1])

# Step 1: Build address and obtain search box half width from command-line input file.
Address = getAddress(StreetNumber, StreetName, AptNumber, City, State, ZipCode)

# Step 2: Get search box coordinates.
NorthBoundary, SouthBoundary, EastBoundary, WestBoundary = getBox(
    Address, SearchBoxHalfWidth
)

# Step 3: Get all sold home Zillow URLs from the user's search box.
SoldHomeZillowLinks = getAllSoldHomeZillowURLs(
    NorthBoundary, SouthBoundary, EastBoundary, WestBoundary, RequestHeaders
)

# Step 4: Create a list containing all sold home data scraped from Zillow URLs.
SoldHomeDataList = scrapeZillowLinks(SoldHomeZillowLinks, RequestHeaders)

# Step 5: Construct pandas dataframe from SoldHomeDataList.
SoldHomeData = soldHomeDF(SoldHomeDataList)
