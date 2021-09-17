import sys


def scrapehomeurls(html, result_count, page_type):
    if page_type.lower() == "zillow":
        # Zillow stores the URL info of each home in the "list-card-info" class
        url_info = html.find_all("div", class_="list-card-info")

        # Zillow automatically recommends additional "relaxed search results" that populate in its page
        # when not many results were returned due to restrictive search criteria (e.g. search area too small).
        # url_info will contain these additional recommended results. However, they are not pertinent
        # to the user defined search box. Therefore, we need to exclude them. Because such a small, restrictive search
        # would return only one page of results, we simply exclude these "recommended relaxed search results" from the
        # unique home urls we actually scrape by looping over the number of actual Zillow results found
        # (which doesn't include the 'recommended relaxed results'), i.e. result_count, or 40, whichever is smaller
        # since the page is limited to 40 results to begin with. However, lets assume we have a search that is large
        # enough to span multiple pages worth of results (i.e. which also means there will be no "recommended relaxed
        # search results" since the search was big enough to begin with), lets say, 42 results. Then on the second page,
        # the length of url_info will now be 2; therefore, we must also take the min of len(url_info) so that
        # we don't get an index out of bounds error.
        urls = []
        for j in range(0, min(result_count, 40, len(url_info)-1)):
            # For each unique home URL, store the href value (actual URL link).
            urls.append(url_info[j].find("a", class_="list-card-link")["href"])
    else:
        sys.exit(
            "ERROR!!! scrapehomeurls.py currently only works for Zillow page types. \n"
            "Please ensure 'Zillow' is being passed as the page_type argument for this function"
        )
    return urls
