from getZillowHTML import getZillowHTML
import webbrowser

def getURLs(NorthBoundary, EastBoundary, SouthBoundary, WestBoundary, req_headers):

    # The Zillow Recently Sold Homes HTML and URL for each page is gathered using getZillowHTML function
    ZillowHTML, ZillowURL = getZillowHTML(
        "Recently Sold",
        None,
        [
            ("North", NorthBoundary),
            ("South", SouthBoundary),
            ("East", EastBoundary),
            ("West", WestBoundary),
        ],
        req_headers
    )

    # Open up the Zillow web page to view the search box, results, and see how many pages there are.
    #webbrowser.open_new(ZillowURL[0]) THIS IS SO ANNOYING!!!

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
            # The Zillow Recently Sold Homes HTML and URL for the subsequent pages is gathered using getZillowHTML function
            ZillowHTML, ZillowURL = getZillowHTML(
                "Recently Sold",
                i,
                [
                    ("North", NorthBoundary),
                    ("South", SouthBoundary),
                    ("East", EastBoundary),
                    ("West", WestBoundary),
                ],
                req_headers
            )

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

    return SoldHomeZillowLinks
