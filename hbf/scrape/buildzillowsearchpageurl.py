import sys


def buildzillowsearchpageurl(
    page_type, page_number, north_boundary, south_boundary, east_boundary, west_boundary
):
    if page_type.lower() == "recently sold":
        if page_number is None or page_number == 0:
            # Construct the Zillow Recently Sold Homes URL (first/initial page) using the search boundary.
            url = (
                "https://www.zillow.com/homes/recently_sold/"
                "?searchQueryState={"
                "pagination:{},"
                "mapBounds:{"
                "west:" + str(west_boundary) + ","
                "east:" + str(east_boundary) + ","
                "south:" + str(south_boundary) + ","
                "north:" + str(north_boundary) + "},"
                "isMapVisible:true,"
                "mapZoom:8,"
                "filterState:{"
                "isForSaleByAgent:{value:false},"
                "isForSaleByOwner:{value:false},"
                "isNewConstruction:{value:false},"
                "isForSaleForeclosure:{value:false},"
                "isComingSoon:{value:false},"
                "isAuction:{value:false},"
                "isPreMarketForeclosure:{value:false},"
                "isPreMarketPreForeclosure:{value:false},"
                "isMakeMeMove:{value:false},"
                "isRecentlySold:{value:true}"
                "},"
                "isListVisible:true}"
            )
        elif page_number > 0:
            # Construct the Zillow Recently Sold Homes URL (subsequent pages) using the search boundary.
            url = (
                "https://www.zillow.com/homes/recently_sold/"
                + str(page_number + 1)
                + "_p/"
                "?searchQueryState={"
                "pagination:{currentPage:" + str(page_number + 1) + "},"
                "mapBounds:{"
                "west:" + str(west_boundary) + ","
                "east:" + str(east_boundary) + ","
                "south:" + str(south_boundary) + ","
                "north:" + str(north_boundary) + "},"
                "isMapVisible:true,"
                "mapZoom:15,"
                "filterState:{"
                "isForSaleByAgent:{value:false},"
                "isForSaleByOwner:{value:false},"
                "isNewConstruction:{value:false},"
                "isForSaleForeclosure:{value:false},"
                "isComingSoon:{value:false},"
                "isAuction:{value:false},"
                "isPreMarketForeclosure:{value:false},"
                "isPreMarketPreForeclosure:{value:false},"
                "isMakeMeMove:{value:false},"
                "isRecentlySold:{value:true}"
                "},"
                "isListVisible:true}"
            )
        else:
            sys.exit(
                "ERROR!!! page_number argument for buildzillowsearchpageurl is not usable"
            )
    else:
        sys.exit(
            "ERROR!!! buildzillowsearchpageurl.py currently only works for 'Recently Sold'-page types. \n"
            "Please ensure 'Recently Sold' is being passed as the page_type argument for this function"
        )
    return url
