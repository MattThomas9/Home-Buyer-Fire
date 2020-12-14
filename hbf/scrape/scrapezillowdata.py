from hbf.scrape.gethtml import gethtml
from progress.bar import IncrementalBar
from hbf.scrape.list2frame import list2frame

# Currently, this scraper function cannot scrape data from Zillow web pages that use
# Java Script to subsequently load webpage details. Java Script transactions on a webpage delay the download
# of information (i.e. details are not shown until user clicks an "expand" button) which results in the
# HTTP request not obtaining a "full" response from the server. Selenium WebDriver could be used as a solution
# to query these JS pages in order to fully acquire all information on a web page.


def scrapezillowdata(zillow_urls, header_input):
    # Initialize progress bar
    bar = IncrementalBar(" Scraping Zillow", max=len(zillow_urls))

    # Initialize list to store home data during loop over each home's Zillow url
    home_data_list = []

    # Loop over each home Zillow URL and scrape pertinent details
    for url in zillow_urls:
        # First, obtain the HTML from the current home Zillow URL using gethtml.py
        home_html = gethtml(url, header_input)

        # The home address is simply taken directly from its own URL.
        home_address = (
            url.replace("https://www.zillow.com/homedetails/", "")
            .replace("-", " ")
            .split("/", 1)[0]
        )

        # First, we search for the home's sell price. In Zillow, this variable is under a
        # "span" class="ds-status-details" tag. The find method will find this variable and store it into a tag
        # (i.e. ds_status_details). Generally, Zillow will show "Sold" and the sell price in this tag. Therefore, we
        # check this tag for the key word "sold" that we know will generally be contained in the tag's text. If the key
        # word is found in the tag's text, then we store the text found in the tag into the appropriate variable while
        # removing the unwanted characters. If the key word is not found, then the appropriate variable will retain its
        # initialization value of "n/a".
        ds_status_details = home_html.find("span", class_="ds-status-details")
        sold_price = "n/a"
        if "sold" in ds_status_details.text.lower():
            sold_price = (
                ds_status_details.text.replace("Sold", "")
                .replace(": $", "")
                .replace(",", "")
            )

        # Next, we search for the number of beds, baths, and the home's square footage. In Zillow, each one of these
        # variables is under a "span" class="ds-bed-bath-living-area" tag. The find_all method will find each one of
        # these variables and store them into a result set (i.e. ds_bed_bath_living_area). Each item of the result set
        # will either contain number of beds and "bd", number of baths and "ba", or the home's size and "Square Feet".
        # We loop over the result set checking each item for key words that we know will be contained in
        # the item's text. If the key word is found in the item's text, then we store the text found in the item into
        # the appropriate variable while removing the unwanted characters. If the key word is not found, then the
        # appropriate variable will retain its initialization value of "n/a".
        ds_bed_bath_living_area = home_html.find_all(
            "span", class_="ds-bed-bath-living-area"
        )
        beds = "n/a"
        baths = "n/a"
        size = "n/a"
        for item in ds_bed_bath_living_area:
            if "bd" in item.text.lower():
                beds = item.text.replace(" bd", "")
                continue
            if "ba" in item.text.lower():
                baths = item.text.replace(" ba", "")
                continue
            if "square feet" in item.text.lower() or "sqft" in item.text.lower():
                size = item.text.replace(",", "").replace("Square Feet", "sqft")
                continue

        # Next, we search for the home type, year built, heating, cooling, parking, and lot size. In Zillow, each one of
        # these variables is under a "li" class="ds-home-fact-list-item" tag. The find_all method will find each one of
        # these variables and store them into a result set (i.e. ds_home_fact_list_items). Each item of the result set
        # has a child "span" class="Text-c11n-8-11-1__aiai24-0 sc-pTWqp jMCspH" tag (i.e. the "label" tag)
        # AND a child "span" class="Text-c11n-8-11-1__aiai24-0 hqfqED" tag (i.e. the "value" tag).
        # For example, for "home type" information (generally the first item in the result set), there will be a
        # "label" tag that will contain the text "Type" and there will be a "value" tag that will contain the text
        # "Single Family". We loop over the result set checking each item's "label" tag for key words that we know will
        # be contained in that tag. If the key word is found in the item's "label" tag, then we store the text found in
        # the item's adjacent "value" tag into the appropriate variable while removing the unwanted characters.
        # If the key word is not found, then the appropriate variable will retain its initialization value of "n/a".
        ds_home_fact_list_items = home_html.find_all(
            "li", class_="ds-home-fact-list-item"
        )
        home_type = "n/a"
        year_built = "n/a"
        heating = "n/a"
        cooling = "n/a"
        parking = "n/a"
        lot_size = "n/a"
        for item in ds_home_fact_list_items:
            if (
                "type"
                in item.find(
                    "span", class_="Text-c11n-8-11-1__aiai24-0 sc-pTWqp jMCspH"
                ).text.lower()
            ):
                home_type = item.find(
                    "span", class_="Text-c11n-8-11-1__aiai24-0 hqfqED"
                ).text
                continue
            if (
                "year built"
                in item.find(
                    "span", class_="Text-c11n-8-11-1__aiai24-0 sc-pTWqp jMCspH"
                ).text.lower()
            ):
                year_built = item.find(
                    "span", class_="Text-c11n-8-11-1__aiai24-0 hqfqED"
                ).text
                continue
            if (
                "heating"
                in item.find(
                    "span", class_="Text-c11n-8-11-1__aiai24-0 sc-pTWqp jMCspH"
                ).text.lower()
            ):
                heating = item.find(
                    "span", class_="Text-c11n-8-11-1__aiai24-0 hqfqED"
                ).text
                continue
            if (
                "cooling"
                in item.find(
                    "span", class_="Text-c11n-8-11-1__aiai24-0 sc-pTWqp jMCspH"
                ).text.lower()
            ):
                cooling = item.find(
                    "span", class_="Text-c11n-8-11-1__aiai24-0 hqfqED"
                ).text
                continue
            if (
                "parking"
                in item.find(
                    "span", class_="Text-c11n-8-11-1__aiai24-0 sc-pTWqp jMCspH"
                ).text.lower()
            ):
                parking = item.find(
                    "span", class_="Text-c11n-8-11-1__aiai24-0 hqfqED"
                ).text
                continue
            if (
                "lot"
                in item.find(
                    "span", class_="Text-c11n-8-11-1__aiai24-0 sc-pTWqp jMCspH"
                ).text.lower()
            ):
                lot_size = item.find(
                    "span", class_="Text-c11n-8-11-1__aiai24-0 hqfqED"
                ).text.replace(",", "")
                continue

        # Append home data information to list
        home_data_list.append(
            [
                home_address,
                sold_price,
                beds,
                baths,
                size,
                home_type,
                year_built,
                heating,
                cooling,
                parking,
                lot_size,
            ]
        )

        bar.next()  # to advance progress bar
    bar.finish()  # to finish the progress bar
    print()  # to add space following progress bar

    # Convert home_data_list into pandas dataframe.
    home_data = list2frame(home_data_list)

    return home_data
