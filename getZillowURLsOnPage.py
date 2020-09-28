

def getZillowURLsOnPage(ZillowHTML, ZillowResultCount):
    # First we find the class where the unique sold homes URLs reside
    SoldHomeZillowLinkInfo = ZillowHTML.find_all("div", class_="list-card-info")

    # Zillow automatically recommends additional "relaxed search results" that populate in its page
    # when not many results were returned due to restrictive search criteria (e.g. search area too small).
    # SoldHomeZillowLinkInfo will contain these additional recommended results. However, they are not pertinent
    # to the user defined search box. Therefore, we need to exclude them. Because such a small, restrictive search
    # would return only one page of results, we simply exclude these "recommended relaxed search results" from the
    # unique sold home links we actually scrape by looping over the number of actual Zillow results found (which doesn't
    # include the 'recommended relaxed results'), i.e. ZillowResultCount, or 40, whichever is smaller since the page
    # is limited to 40 results to begin with.
    # However, lets assume we have a search that is large enough to span multiple pages worth of results (i.e. which
    # also means there will be no "recommended relaxed search results" since the search was big enough to begin with),
    # lets say, 42 results. Then on the second page, the length of SoldHomeZillowLinkInfo will now be 2; therefore,
    # we must also take the min of SoldHomeZillowLinkInfo so that we don't get an index out of bounds error.
    links = []
    for j in range(0, min(ZillowResultCount, 40, len(SoldHomeZillowLinkInfo))):
        # For each unique sold home URL, store the href value (actual URL link).
        links.append(SoldHomeZillowLinkInfo[j].find("a", class_="list-card-link")["href"])
    return links
