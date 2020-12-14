import sys
from hbf.helpers.logtofile import logtofile


def scraperesultcount(html, page_type, zillow_max_result):
    if page_type.lower() == "zillow":
        # Zillow keeps the result count in the "result-count" class
        result_count = int(
            (html.find("span", class_="result-count")).text.split()[0].replace(",", "")
        )
        mess = (
            str(result_count)
            + " Zillow search results were found within the search box."
        )
        logtofile(__name__, mess, "INFO")
        # Zillow limits the number of pages of a search to 20, and the number of results/page to 40.
        # Therefore, the maximum number of results one can obtain is 800.
        if result_count > zillow_max_result:
            mess = (
                "Warning! The maximum number of Zillow search results was met or exceeded. \n"
                "Therefore, only the first "
                + str(zillow_max_result)
                + " search result links will be scraped."
            )
            logtofile(__name__, mess, "INFO")
            result_count = zillow_max_result
    else:
        sys.exit(
            "ERROR!!! scraperesultcount.py currently only works for Zillow page types. \n"
            "Please ensure 'Zillow' is being passed as the page_type argument for this function"
        )
    return result_count
