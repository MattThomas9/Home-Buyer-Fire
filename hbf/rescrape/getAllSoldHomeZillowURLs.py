from rescrape.buildZillowURL import buildZillowURL
from rescrape.getHTML import getHTML
from rescrape.getNumZillowPages import getNumZillowPages
from rescrape.getNumZillowResults import getNumZillowResults
from rescrape.getZillowURLsOnPage import getZillowURLsOnPage
import webbrowser


def getAllSoldHomeZillowURLs(
    NorthBoundary, SouthBoundary, EastBoundary, WestBoundary, RequestHeaders
):

    # The Zillow Recently Sold Homes URL for the first/initial search page is constructed with buildZillowURL.py
    ZillowURL = buildZillowURL(
        "Recently Sold", None, NorthBoundary, SouthBoundary, EastBoundary, WestBoundary
    )

    # Using the ZillowURL, its HTML is requested and parsed using getHTML function
    ZillowHTML = getHTML(ZillowURL, RequestHeaders)

    # Open up the Zillow web page to view the search box, results, and see how many pages there are.
    # webbrowser.open_new(ZillowURL)  # AMRIT IS SO ANNOYING!!!

    # Find the number of pages of results associated with the Zillow search box.
    NumZillowPages = getNumZillowPages(ZillowHTML)

    # Find the total number of Zillow results, and store as an integer.
    ZillowResultCount = getNumZillowResults(ZillowHTML)

    # Loop over the number of pages found from the original Zillow search to obtain each
    # unique recently sold home link from each page.
    SoldHomeZillowLinks = []
    for i in range(0, NumZillowPages):
        if i == 0:
            # The page one URL was already requested and parsed above; therefore, we scrape it to
            # get all of the unique sold homes' URLs.
            SoldHomeZillowLinks.extend(
                getZillowURLsOnPage(ZillowHTML, ZillowResultCount)
            )

        else:
            # For each page after page one, the Zillow URL must be constructed, requested, parsed, and scraped.
            # The Zillow Recently Sold Homes URL for the subsequent search pages is constructed with buildZillowURL.py
            ZillowURL = buildZillowURL(
                "Recently Sold",
                i,
                NorthBoundary,
                SouthBoundary,
                EastBoundary,
                WestBoundary,
            )

            # Using the ZillowURL, its HTML is requested and parsed using getHTML function
            ZillowHTML = getHTML(ZillowURL, RequestHeaders)

            # Scrape the current Zillow search result page to obtain all unique sold homes' URLs.
            SoldHomeZillowLinks.extend(
                getZillowURLsOnPage(ZillowHTML, ZillowResultCount)
            )

    # All unique Sold Home Zillow URLs from the user's search box are printed to screen, in case the user needs to
    # quickly visit any one of them.
    print(*SoldHomeZillowLinks, sep="\n")

    # An equality check is completed to make sure the number of SoldHomeZillowLinks is the same as
    # the ZillowResultCount. The number of SoldHomeZillowLinks is a count of each unique sold home link we scraped.
    # The ZillowResultCount is the total number of search results from the original Zillow search web page. If they are
    # not equal, it may mean more or less sold home URLs have been scraped than what the original Zillow search result
    # count was from the original Zillow web page, thus indicating a potential error.
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

    return SoldHomeZillowLinks
