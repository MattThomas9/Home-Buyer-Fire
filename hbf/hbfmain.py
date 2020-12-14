from hbf.helpers.logtofile import logtofile
import time
from hbf.preprocess.getinput import getinput
from hbf.preprocess.buildaddress import buildaddress
from hbf.preprocess.buildsearchbox import buildsearchbox
from hbf.scrape.getzillowurls import getzillowurls
from hbf.scrape.scrapezillowdata import scrapezillowdata
from hbf.dataclean.laundry import laundry


def hbfmain(inp):

    start_time = time.time()
    logtofile(__name__, "Started.", "INFO")

    # Step 0: Get input parameters from input file.
    (
        street_number,
        street_name,
        apt_number,
        city,
        state,
        zip_code,
        search_box_half_width,
        zillow_max_result,
        zillow_req_headers,
    ) = getinput(inp)

    # Step 1: Build address.
    address = buildaddress(
        street_number, street_name, apt_number, city, state, zip_code
    )

    # Step 2: Get search box coordinates.
    north_boundary, south_boundary, east_boundary, west_boundary = buildsearchbox(
        address, search_box_half_width
    )

    # Step 3: Get all recently sold home Zillow URLs from the user's search box.
    sold_zillow_urls = getzillowurls(
        "Recently Sold",
        north_boundary,
        south_boundary,
        east_boundary,
        west_boundary,
        zillow_max_result,
        zillow_req_headers,
    )

    # Step 4: Scrape data from Zillow URLS into a pandas dataframe.
    sold_zillow_data = scrapezillowdata(sold_zillow_urls, zillow_req_headers)

    # Step 5: Clean the data frame
    sold_zillow_data_cleaned = laundry(sold_zillow_data)

    # Step 6: Analyze the data
    # ------
    # to be completed by adding regression analysis to predict sold home price
    # ------

    # Log timing info.
    logtofile(__name__, "Finished.", "INFO")
    mess = str("--- %s seconds ---" % (time.time() - start_time))
    logtofile(__name__, mess, "INFO")
    print(mess)

    return sold_zillow_data_cleaned
