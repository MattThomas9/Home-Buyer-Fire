from hbf.helpers.logger import logToFile
import sys
import time
from hbf.rescrape.getInput import getInput
from hbf.rescrape.getAddress import getAddress
from hbf.rescrape.getBox import getBox
from hbf.rescrape.getAllSoldHomeZillowURLs import getAllSoldHomeZillowURLs
from hbf.rescrape.scrapeZillowLinks import scrapeZillowLinks
from hbf.rescrape.soldHomeDF import soldHomeDF
from hbf.rescrape.laundry import laundry


def getDF(inp):

    startTime = time.time()
    logToFile(__name__, "Started.", "INFO")
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
    ) = getInput(inp)

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

    # Step 6: Clean the SoldHomeData data frame
    SoldHomeData_cleaned = laundry(SoldHomeData)
    logToFile(__name__, "Finished.", "INFO")

    # Log timing info.
    mess = str("--- %s seconds ---" % (time.time() - startTime))
    logToFile(__name__, mess, "INFO")
    print("--- %s seconds ---" % (time.time() - startTime))

    return SoldHomeData_cleaned
