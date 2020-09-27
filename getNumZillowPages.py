

def getNumZillowPages(ZillowHTML):
    # Search through the ZillowHTML to try and find the class where page numbers are kept
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
    return NumZillowPages
