import sys
from hbf.helpers.logtofile import logtofile


def scrapepagecount(html, page_type):
    if page_type.lower() == "zillow":
        # Zillow keeps the page numbers in the "search-pagination" class
        page_list = html.find("div", class_="search-pagination")
        if page_list is None:
            mess = "Only 1 page of Zillow search results exist in this search box."
            logtofile(__name__, mess, "INFO")
            page_count = 1
        else:
            page_links = page_list.find_all("a")
            mess = (
                str(page_links[-2].text)
                + " pages of Zillow search results exist in this search box."
            )
            logtofile(__name__, mess, "INFO")
            page_count = int(page_links[-2].text)
    else:
        sys.exit(
            "ERROR!!! scrapepagecount.py currently only works for Zillow page types. \n"
            "Please ensure 'Zillow' is being passed as the page_type argument for this function"
        )
    return page_count
