import requests
from bs4 import BeautifulSoup

def scrapeZillowLinks(SoldHomeZillowLinks, req_headers):
    # Initialize list to hold sold home data during loop over each recently sold home Zillow link
    SoldHomeDataList = []

    # Loop over each recently sold home Zillow URL and scrape pertinent sold home details
    for i in range(0, len(SoldHomeZillowLinks)):

        # Send an HTTP request to the Zillow URL to obtain the raw HTML data, using the same headers defined above.
        with requests.Session() as s:
            r = s.get(SoldHomeZillowLinks[i], headers=req_headers)
        # Parse the raw HTML data from the Zillow URL request using Beautiful Soup.
        ZillowHTML = BeautifulSoup(r.content, "html.parser")

        # Scrape the current Zillow page to obtain the sold homes' details and information (e.g. address, price, size, etc).
        # The sold home address is simply taken directly from its own URL.
        SoldHomeAddress = (
            SoldHomeZillowLinks[i]
            .replace("https://www.zillow.com/homedetails/", "")
            .replace("-", " ")
            .split("/", 1)[0]
        )

        # We try to find the SoldHomePrice using a try-except statement because in some cases the HTML tag/class we are
        # searching for does not exist, which means the ZillowHTML.find() will return None, and the subsequent .find()
        # on a NoneType throws an AttributeError. When this AttributeError is thrown, we store "n/a" into the SoldHomePrice
        # variable.
        # Currently, this scraper cannot scrape information from Zillow web pages that use Java Script to subsequently load
        # webpage details. Java Script transactions on a webpage delay the download of information (i.e. details are not
        # shown until user clicks an "expand" button) which results in the HTTP request not obtaining a "full" response from
        # the server. Selenium WebDriver could be used as a solution to query these JS pages in order to fully acquire all
        # information on a web page.
        try:
            SoldHomePrice = (
                ZillowHTML.find("div", class_="ds-home-details-chip")
                .find("p")
                .text.split()[1]
                .replace("$", "")
                .replace(",", "")
                .replace("Sold", "")
            )
        except AttributeError:
            SoldHomePrice = "n/a"
        # Next, we search for the number of beds, baths, and the home's square footage. These items are scraped and stored
        # in Home_Size_items using a try-except statement for the same reasons discussed above. In this case, when an
        # AttributeError is thrown, we store an empty list into Home_Size_items, which will cause the subsequent try-except
        # statements to throw an IndexError, which will ultimately cause "n/a" to be stored for the number of beds, baths,
        # and/or sqft.
        try:
            Home_Size_container = ZillowHTML.find(
                "h3", class_="ds-bed-bath-living-area-container"
            )
            Home_Size_items = []
            for item in Home_Size_container.select(
                ".ds-bed-bath-living-area span:not(.ds-vertical-divider)"
            ):
                Home_Size_items.append(item.text)
        except AttributeError:
            Home_Size_items = []
        # Now, for each item in Home_Size_items, we look for the words "bd", "ba", and "Square Feet", which is what Zillow
        # uses to label number of beds, baths, and square footage. If we find these key words, we obtain that element's
        # position in the list (i.e. its index). We know that the element in front of each key word is the actual value.
        # For example, if "bd" is found in the Home_Size_items list, and it's index = 2, then we know the actual value for
        # the number of beds is contained in the Home_Size_items list at index 1. The associated value is then stored in the
        # appropriate variable. The try-except statement is used so that if "bd", "ba", or "Square Feet" is not found
        # (i.e. possibly because the web page we are currently scraping is actually for a recently sold parcel of land that
        # only obviously shows the square footage), an IndexError is thrown, and "n/a" is stored instead. Or, if
        # Home_Size_items is an empty list (see above), an IndexError will also be thrown, and "n/a" will be stored.
        try:
            index = [j for j, x in enumerate(Home_Size_items) if "bd" in x.lower()]
            SoldHomeBeds = Home_Size_items[index[0] - 1]
        except IndexError:
            SoldHomeBeds = "n/a"
        try:
            index = [j for j, x in enumerate(Home_Size_items) if "ba" in x.lower()]
            SoldHomeBaths = Home_Size_items[index[0] - 1]
        except IndexError:
            SoldHomeBaths = "n/a"
        try:
            index = [j for j, x in enumerate(Home_Size_items) if "square feet" in x.lower()]
            SoldHomeSqFt = Home_Size_items[index[0] - 1]
        except IndexError:
            SoldHomeSqFt = "n/a"
        # Next, we search for the home type, year built, heating, cooling, parking, and lot size details of the house.
        # These details, or "facts" as Zillow calls them, are contained within a fact-label class and a fact-value class.
        # The labels and values are stored accordingly using a try-except statement because in some cases the information
        # cannot be found and thus a "n/a" needs to be stored instead (e.g. the web page we are scraping is of a recently
        # sold parcel of land with no actual home on it, so information like "year built" does not exist). If the labels and
        # values cannot be found, the ZillowHTML.find() will return None, and the .find_all() on a NoneType throws an
        # AttributeError. When this AttributeError is thrown, "n/a" is stored into the type, year built, heating, cooling,
        # parking, and lot size variables.
        # 9/20/2020 - updated classes in below .find() statements to account for new zillow layout
        try:
            SoldHomeFactLabels = ZillowHTML.find("ul", class_="ds-home-fact-list").find_all(
                "span", class_="ds-home-fact-label"
            )
            SoldHomeFactValues = ZillowHTML.find("ul", class_="ds-home-fact-list").find_all(
                "span", class_="ds-home-fact-value"
            )
        except AttributeError:
            SoldHomeType = "n/a"
            SoldHomeYearBuilt = "n/a"
            SoldHomeHeating = "n/a"
            SoldHomeCooling = "n/a"
            SoldHomeParking = "n/a"
            SoldHomeLotSize = "n/a"
        # If there is information in SoldHomeFactLabels and SoldHomeFactValues, such that the above error is not
        # thrown, the following else statement is executed.
        else:
            # Within SoldHomeFactLabels, we try to find each specific label's index (e.g. what position is the "year built"
            # label inside SoldHomeFactLabels). Subsequently, using that index, we know the label's corresponding value
            # (e.g. 1969) has the same index but is obviously located in SoldHomeFactValues. So if the index of "year built"
            # in SoldHomeFactLabels is 2, we know that the index of its corresponding value, 1969, in SoldHomeFactValues is
            # also 2. The values of these labels are thus stored into the appropriate variables. If we cannot find the
            # specific label within SoldHomeFactLabels, the index variable becomes an empty list, and when that empty list
            # is referenced in the following statement for storing the actual value, an IndexError will be thrown and "n/a"
            # will be stored instead.
            try:
                index = [
                    j for j, x in enumerate(SoldHomeFactLabels) if "type" in x.text.lower()
                ]
                SoldHomeType = SoldHomeFactValues[index[0]].text
            except IndexError:
                SoldHomeType = "n/a"
            try:
                index = [
                    j
                    for j, x in enumerate(SoldHomeFactLabels)
                    if "year built" in x.text.lower()
                ]
                SoldHomeYearBuilt = SoldHomeFactValues[index[0]].text
            except IndexError:
                SoldHomeYearBuilt = "n/a"
            try:
                index = [
                    j
                    for j, x in enumerate(SoldHomeFactLabels)
                    if "heating" in x.text.lower()
                ]
                SoldHomeHeating = SoldHomeFactValues[index[0]].text
            except IndexError:
                SoldHomeHeating = "n/a"
            try:
                index = [
                    j
                    for j, x in enumerate(SoldHomeFactLabels)
                    if "cooling" in x.text.lower()
                ]
                SoldHomeCooling = SoldHomeFactValues[index[0]].text
            except IndexError:
                SoldHomeCooling = "n/a"
            try:
                index = [
                    j
                    for j, x in enumerate(SoldHomeFactLabels)
                    if "parking" in x.text.lower()
                ]
                SoldHomeParking = SoldHomeFactValues[index[0]].text
            except IndexError:
                SoldHomeParking = "n/a"
            try:
                index = [
                    j for j, x in enumerate(SoldHomeFactLabels) if "lot" in x.text.lower()
                ]
                SoldHomeLotSize = SoldHomeFactValues[index[0]].text
            except IndexError:
                SoldHomeLotSize = "n/a"

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
                SoldHomeLotSize
            ]
        )

    return SoldHomeDataList
