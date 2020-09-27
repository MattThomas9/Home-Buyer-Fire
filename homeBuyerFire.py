import sys
from getAddress import getAddress
from getBox import getBox
from getAllSoldHomeZillowURLs import getAllSoldHomeZillowURLs
from scrapeZillowLinks import scrapeZillowLinks
from soldHomeDF import soldHomeDF

# Step 1: Build address and obtain search box half width from command-line input file.
Address, SearchBoxHalfWidth = getAddress(sys.argv[1])

# Step 2: Get search box coordinates.
NorthBoundary, EastBoundary, SouthBoundary, WestBoundary = getBox(
    Address, SearchBoxHalfWidth
)

# Step 3: Get all sold home Zillow URLs from the user's search box.
SoldHomeZillowLinks = getAllSoldHomeZillowURLs(
                        NorthBoundary,
                        EastBoundary,
                        SouthBoundary,
                        WestBoundary
                      )

# Step 4: Create a list containing all sold home data scraped from Zillow URLs.
SoldHomeDataList = scrapeZillowLinks(SoldHomeZillowLinks)

# Step 5: Construct pandas dataframe from SoldHomeDataList.
SoldHomeData = soldHomeDF(SoldHomeDataList)
