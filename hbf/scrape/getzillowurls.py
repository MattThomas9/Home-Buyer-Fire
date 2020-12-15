from hbf.helpers.logtofile import logtofile
from hbf.scrape.buildzillowsearchpageurl import buildzillowsearchpageurl
from hbf.scrape.gethtml import gethtml
from hbf.scrape.scrapepagecount import scrapepagecount
from hbf.scrape.scraperesultcount import scraperesultcount
from hbf.scrape.scrapehomeurls import scrapehomeurls


def getzillowurls(
    page_type,
    north_boundary,
    south_boundary,
    east_boundary,
    west_boundary,
    zillow_max_result,
    zillow_req_headers,
):
    # The first/initial Zillow search page url is constructed with buildzillowsearchpageurl.py
    zillow_search_page_url = buildzillowsearchpageurl(
        page_type, None, north_boundary, south_boundary, east_boundary, west_boundary
    )

    # Open up the Zillow search page to view the search box, results, and see how many pages there are.
    # import webbrowser
    # webbrowser.open_new(zillow_search_page_url)

    # Using the zillow_search_page_url, its HTML is requested and parsed using gethtml function
    zillow_search_page_html = gethtml(zillow_search_page_url, zillow_req_headers)

    # Find the total number of pages of results on this first/initial Zillow search page.
    zillow_page_count = scrapepagecount(zillow_search_page_html, "Zillow")

    # Find the total number of Zillow results.
    zillow_result_count = scraperesultcount(
        zillow_search_page_html, "Zillow", zillow_max_result
    )

    # Loop over the number of pages found from the original Zillow search to obtain each home's unique url.
    zillow_home_urls = []
    for i in range(0, zillow_page_count):
        if i == 0:
            # The page one search URL was already requested and parsed above; therefore, we scrape it to
            # get all of the unique home URLs on this page.
            zillow_home_urls.extend(
                scrapehomeurls(zillow_search_page_html, zillow_result_count, "Zillow")
            )

        else:
            # For each page after page one, the Zillow search page URL must be constructed, requested, parsed, and
            # scraped.
            zillow_search_page_url = buildzillowsearchpageurl(
                page_type,
                i,
                north_boundary,
                south_boundary,
                east_boundary,
                west_boundary,
            )

            # Using the zillow_search_page_url, its HTML is requested and parsed using gethtml function
            zillow_search_page_html = gethtml(
                zillow_search_page_url, zillow_req_headers
            )

            # Scrape the current Zillow search page to obtain all unique home URLs.
            zillow_home_urls.extend(
                scrapehomeurls(zillow_search_page_html, zillow_result_count, "Zillow")
            )

    # All unique home URLs are printed to log, in case the user needs to quickly visit any one of them.
    mess = "\n".join(zillow_home_urls)
    logtofile(__name__, mess, "INFO")

    # An equality check is completed to make sure the number of zillow_home_urls is the same as the
    # zillow_result_count. The number of zillow_home_urls is a count of each unique home url we scraped. The
    # zillow_result_count is the total number of search results from the original Zillow search web page. If they are
    # not equal, it may mean more or less home URLs have been scraped than what the original Zillow search result
    # count was from the original Zillow web page, thus indicating a potential error.
    if len(zillow_home_urls) == zillow_result_count:
        mess = (
            "The number of unique home urls scraped from all pages equals \n"
            "the Zillow Result Count that was scraped from the initial page."
        )
        logtofile(__name__, mess, "INFO")
    else:
        mess = (
            "WARNING!!! The number of unique home urls scraped from all pages DOES NOT EQUAL \n"
            "the Zillow Result Count that was scraped from the initial page. There may be an issue with Zillow \n"
            "recommending/providing additional urls on subsequent pages that weren't originally included in \n"
            "the Zillow Result Count, or additional pages of results were not scraped because they are hidden \n"
            "behind Java Script."
        )
        logtofile(__name__, mess, "WARNING")

    return zillow_home_urls
