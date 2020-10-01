import sys


def buildZillowURL(PageType, PageNumber, NorthBoundary, SouthBoundary, EastBoundary, WestBoundary):
    if PageType.lower() == "recently sold":
        if PageNumber is None or PageNumber == 0:
            # Construct the Zillow Recently Sold Homes URL (first/initial page) using the search boundary.
            ZillowURL = "https://www.zillow.com/homes/recently_sold/" \
                        "?searchQueryState={" \
                        "pagination:{}," \
                        "mapBounds:{" \
                        "west:" + str(WestBoundary) + \
                        "," \
                        "east:" + str(EastBoundary) + \
                        "," \
                        "south:" + str(SouthBoundary) + \
                        "," \
                        "north:" + str(NorthBoundary) + \
                        "}," \
                        "isMapVisible:true," \
                        "mapZoom:8," \
                        "filterState:{" \
                        "isForSaleByAgent:{value:false}," \
                        "isForSaleByOwner:{value:false}," \
                        "isNewConstruction:{value:false}," \
                        "isForSaleForeclosure:{value:false}," \
                        "isComingSoon:{value:false}," \
                        "isAuction:{value:false}," \
                        "isPreMarketForeclosure:{value:false}," \
                        "isPreMarketPreForeclosure:{value:false}," \
                        "isMakeMeMove:{value:false}," \
                        "isRecentlySold:{value:true}" \
                        "}," \
                        "isListVisible:true}"
        elif PageNumber > 0:
            # Construct the Zillow Recently Sold Homes URL (subsequent pages) using the search boundary.
            ZillowURL = "https://www.zillow.com/homes/recently_sold/" \
                        + str(PageNumber + 1) + \
                        "_p/" \
                        "?searchQueryState={" \
                        "pagination:{currentPage:" + \
                        str(PageNumber + 1) + \
                        "}," \
                        "mapBounds:{" \
                        "west:" + str(WestBoundary) + \
                        "," \
                        "east:" + str(EastBoundary) + \
                        "," \
                        "south:" + str(SouthBoundary) + \
                        "," \
                        "north:" + str(NorthBoundary) + \
                        "}," \
                        "isMapVisible:true," \
                        "mapZoom:15," \
                        "filterState:{" \
                        "isForSaleByAgent:{value:false}," \
                        "isForSaleByOwner:{value:false}," \
                        "isNewConstruction:{value:false}," \
                        "isForSaleForeclosure:{value:false}," \
                        "isComingSoon:{value:false}," \
                        "isAuction:{value:false}," \
                        "isPreMarketForeclosure:{value:false}," \
                        "isPreMarketPreForeclosure:{value:false}," \
                        "isMakeMeMove:{value:false}," \
                        "isRecentlySold:{value:true}" \
                        "}," \
                        "isListVisible:true}"
        else:
            sys.exit("ERROR!!! PageNumber argument for buildZillowURL is not usable")
    else:
        sys.exit("ERROR!!! buildZillowURL.py currently only works for 'Recently Sold'-page types. \n"
                 "Please ensure 'Recently Sold' is being passed as the PageType argument for this function")
    return ZillowURL
