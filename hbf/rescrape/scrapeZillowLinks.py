from hbf.rescrape.getHTML import getHTML
from progress.bar import IncrementalBar

# Currently, this scraper function cannot scrape information from Zillow web pages that use
# Java Script to subsequently load webpage details. Java Script transactions on a webpage delay the download
# of information (i.e. details are not shown until user clicks an "expand" button) which results in the
# HTTP request not obtaining a "full" response from the server. Selenium WebDriver could be used as a solution
# to query these JS pages in order to fully acquire all information on a web page.


def scrapeZillowLinks(SoldHomeZillowLinks, headerInput):
    # Initialize progress bar
    bar = IncrementalBar(" Scraping Zillow", max=len(SoldHomeZillowLinks))

    # Initialize list to hold sold home data during loop over each recently sold home Zillow link
    SoldHomeDataList = []

    # Loop over each recently sold home Zillow URL and scrape pertinent sold home details
    for link in SoldHomeZillowLinks:
        # First, obtain the HTML from the current Sold Home Zillow URL using getHTML.py
        ZillowHTML = getHTML(link, headerInput)

        # The sold home address is simply taken directly from its own URL.
        SoldHomeAddress = (
            link.replace("https://www.zillow.com/homedetails/", "")
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
        ds_status_details = ZillowHTML.find("span", class_="ds-status-details")
        SoldHomePrice = "n/a"
        if "sold" in ds_status_details.text.lower():
            SoldHomePrice = (
                ds_status_details.text.replace("Sold", "")
                .replace(": $", "")
                .replace(",", "")
            )

        # Next, we search for the number of beds, baths, and the home's square footage. In Zillow, each one of these
        # variables is under a "span" class="ds-bed-bath-living-area" tag. The find_all method will find each one of
        # these variables and store them into a result set (i.e. ds_bed_bath_living_area). Each item of the result set
        # will either contain number of beds and "bd", number of baths and "ba", or the home's square footage and
        # "Square Feet". We loop over the result set checking each item for key words that we know will be contained in
        # the item's text. If the key word is found in the item's text, then we store the text found in the item into
        # the appropriate variable while removing the unwanted characters. If the key word is not found, then the
        # appropriate variable will retain its initialization value of "n/a".
        ds_bed_bath_living_area = ZillowHTML.find_all(
            "span", class_="ds-bed-bath-living-area"
        )
        SoldHomeBeds = "n/a"
        SoldHomeBaths = "n/a"
        SoldHomeSqFt = "n/a"
        for item in ds_bed_bath_living_area:
            if "bd" in item.text.lower():
                SoldHomeBeds = item.text.replace(" bd", "")
                continue
            if "ba" in item.text.lower():
                SoldHomeBaths = item.text.replace(" ba", "")
                continue
            if "square feet" in item.text.lower() or "sqft" in item.text.lower():
                SoldHomeSqFt = item.text.replace(",", "").replace("Square Feet", "sqft")
                continue

        # Next, we search for the home type, year built, heating, cooling, parking, and lot size. In Zillow, each one of
        # these variables is under a "li" class="ds-home-fact-list-item" tag. The find_all method will find each one of
        # these variables and store them into a result set (i.e. ds_home_fact_list_items). Each item of the result set
        # has a child "span" class="Text-c11n-8-11-1__aiai24-0 sc-pLwIe gSdGFm" tag (i.e. the "label" tag)
        # AND a child "span" class="Text-c11n-8-11-1__aiai24-0 hqfqED" tag (i.e. the "value" tag).
        # For example, for "home type" information (generally the first item in the result set), there will be a
        # "label" tag that will contain the text "Type" and there will be a "value" tag that will contain the text
        # "Single Family". We loop over the result set checking each item's "label" tag for key words that we know will
        # be contained in that tag. If the key word is found in the item's "label" tag, then we store the text found in
        # the item's adjacent "value" tag into the appropriate variable while removing the unwanted characters.
        # If the key word is not found, then the appropriate variable will retain its initialization value of "n/a".
        ds_home_fact_list_items = ZillowHTML.find_all(
            "li", class_="ds-home-fact-list-item"
        )
        SoldHomeType = "n/a"
        SoldHomeYearBuilt = "n/a"
        SoldHomeHeating = "n/a"
        SoldHomeCooling = "n/a"
        SoldHomeParking = "n/a"
        SoldHomeLotSize = "n/a"
        for item in ds_home_fact_list_items:
            if (
                "type"
                in item.find(
                    "span", class_="Text-c11n-8-11-1__aiai24-0 sc-pTWqp jMCspH"
                ).text.lower()
            ):
                SoldHomeType = item.find(
                    "span", class_="Text-c11n-8-11-1__aiai24-0 hqfqED"
                ).text
                continue
            if (
                "year built"
                in item.find(
                    "span", class_="Text-c11n-8-11-1__aiai24-0 sc-pTWqp jMCspH"
                ).text.lower()
            ):
                SoldHomeYearBuilt = item.find(
                    "span", class_="Text-c11n-8-11-1__aiai24-0 hqfqED"
                ).text
                continue
            if (
                "heating"
                in item.find(
                    "span", class_="Text-c11n-8-11-1__aiai24-0 sc-pTWqp jMCspH"
                ).text.lower()
            ):
                SoldHomeHeating = item.find(
                    "span", class_="Text-c11n-8-11-1__aiai24-0 hqfqED"
                ).text
                continue
            if (
                "cooling"
                in item.find(
                    "span", class_="Text-c11n-8-11-1__aiai24-0 sc-pTWqp jMCspH"
                ).text.lower()
            ):
                SoldHomeCooling = item.find(
                    "span", class_="Text-c11n-8-11-1__aiai24-0 hqfqED"
                ).text
                continue
            if (
                "parking"
                in item.find(
                    "span", class_="Text-c11n-8-11-1__aiai24-0 sc-pTWqp jMCspH"
                ).text.lower()
            ):
                SoldHomeParking = item.find(
                    "span", class_="Text-c11n-8-11-1__aiai24-0 hqfqED"
                ).text
                continue
            if (
                "lot"
                in item.find(
                    "span", class_="Text-c11n-8-11-1__aiai24-0 sc-pTWqp jMCspH"
                ).text.lower()
            ):
                SoldHomeLotSize = item.find(
                    "span", class_="Text-c11n-8-11-1__aiai24-0 hqfqED"
                ).text.replace(",", "")
                continue

        # Append SoldHome information to list
        SoldHomeDataList.append(
            [
                SoldHomeAddress,
                SoldHomePrice,
                SoldHomeBeds,
                SoldHomeBaths,
                SoldHomeSqFt,
                SoldHomeType,
                SoldHomeYearBuilt,
                SoldHomeHeating,
                SoldHomeCooling,
                SoldHomeParking,
                SoldHomeLotSize,
            ]
        )

        bar.next()  # to advance progress bar
    bar.finish()  # to finish the progress bar
    print()  # to add space following progress bar

    return SoldHomeDataList
