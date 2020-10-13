from helpers.logger import logToFile


def getNumZillowPages(ZillowHTML):
    # Search through the ZillowHTML to try and find the class where page numbers are kept
    ZillowPageList = ZillowHTML.find("div", class_="search-pagination")
    if ZillowPageList is None:
        mess = "Only 1 page of Zillow search results exist in this search box."
        logToFile(__name__, mess, "INFO")
        NumZillowPages = 1
    else:
        ZillowPageLinks = ZillowPageList.find_all("a")
        mess = (
            str(ZillowPageLinks[-2].text)
            + " pages of Zillow search results exist in this search box."
        )
        logToFile(__name__, mess, "INFO")
        NumZillowPages = int(ZillowPageLinks[-2].text)
    return NumZillowPages
