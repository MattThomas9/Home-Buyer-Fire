from getHTML import getHTML


# Currently, this scraper function cannot scrape information from Zillow web pages that use
# Java Script to subsequently load webpage details. Java Script transactions on a webpage delay the download
# of information (i.e. details are not shown until user clicks an "expand" button) which results in the
# HTTP request not obtaining a "full" response from the server. Selenium WebDriver could be used as a solution
# to query these JS pages in order to fully acquire all information on a web page.

def scrapeZillowLinks(SoldHomeZillowLinks, headerInput):
    # Initialize list to hold sold home data during loop over each recently sold home Zillow link
    SoldHomeDataList = []

    # Loop over each recently sold home Zillow URL and scrape pertinent sold home details
    for link in SoldHomeZillowLinks:
        # First, obtain the HTML from the current Sold Home Zillow URL using getHTML.py
        ZillowHTML = getHTML(link, headerInput)

        # The sold home address is simply taken directly from its own URL.
        SoldHomeAddress = (
            link
            .replace("https://www.zillow.com/homedetails/", "")
            .replace("-", " ")
            .split("/", 1)[0]
        )

        # First, we search for the home's sell price. We use a try/except query in case the search for the sell price
        # comes back none/empty. For the sold home price, ZillowHTML.find("span", class_="ds-status-details") searches
        # for the Zillow HTML "span" tag and "ds-status-details" class. If this tag and class are found, the sold home
        # price is scraped by obtaining the text of the result and removing unwanted characters. If this tag and class
        # are not found, the .find() method will return a NoneType. Subsequently, the .text method on a NoneType raises
        # an AttributeError exception, where "n/a" is then stored into the SoldHomePrice variable.
        ds_status_details = ZillowHTML.find("span", class_="ds-status-details")
        try:
            SoldHomePrice = ds_status_details.text.replace(
                "Sold: $", ""
            ).replace(
                ",", ""
            )
        except AttributeError:
            SoldHomePrice = "n/a"

        # Next, we search for the number of beds, baths, and the home's square footage. We use a try/except query in
        # case the search for this information comes back none/empty. For this information,
        # ZillowHTML.find_all("span", class_="ds-bed-bath-living-area") searches for the Zillow HTML "span" tag and
        # "ds-bed-bath-living-area" class. If this tag and class are found, the number of beds, baths, and square
        # footage is scraped by obtaining the text of the result, where the result (i.e. ds_bed_bath_living_area) is a
        # python ResultSet such that ds_bed_bath_living_area[0] contains number of beds, ds_bed_bath_living_area[1]
        # contains number of baths, and ds_bed_bath_living_area[2] contains square footage, and removing unwanted
        # characters. If this tag and class are not found, the .find_all() method will return an empty ResultSet.
        # Subsequently, trying to access the [0]th, [1]st, or [2]nd index of an empty ResultSet raises an IndexError
        # exception, where "n/a" is then stored into the SoldHomeBeds, SoldHomeBaths, and SoldHomeSqFt variables.
        ds_bed_bath_living_area = ZillowHTML.find_all("span", class_="ds-bed-bath-living-area")
        try:
            SoldHomeBeds = ds_bed_bath_living_area[0].text.replace(
                " bd", ""
            )
        except IndexError:
            SoldHomeBeds = "n/a"

        try:
            SoldHomeBaths = ds_bed_bath_living_area[1].text.replace(
                " ba", ""
            )
        except IndexError:
            SoldHomeBaths = "n/a"

        try:
            SoldHomeSqFt = ds_bed_bath_living_area[2].text.replace(
                ",", ""
            ).replace(
                "Square Feet", "SqFt"
            )
        except IndexError:
            SoldHomeSqFt = "n/a"

        # Next, we search for the home type, year built, heating, cooling, parking, and lot size. We use a try/except
        # query in case the search for this information comes back none/empty. For this information,
        # ZillowHTML.find_all("li", class_="ds-home-fact-list-item") searches for the Zillow HTML "li" tag and
        # "ds-home-fact-list-item" class. If this tag and class are found, the home type, year built, heating type,
        # cooling type, parking type, and lot size are scraped by obtaining the text of the result, where the result
        # (i.e. ds_home_fact_list_item) is a python ResultSet such that ds_home_fact_list_item[0] contains home type,
        # ds_home_fact_list_item[1] contains year built, ds_home_fact_list_item[2] contains heating type,
        # ds_home_fact_list_item[3] contains cooling type, ds_home_fact_list_item[4] contains parking type,
        # and ds_home_fact_list_item[5] contains the lot size, and removing unwanted characters. If this tag and class
        # are not found, the .find_all() method will return an empty ResultSet. Subsequently, trying to access the
        # [0]th, [1]st, [2]nd, ..., or [n]th index of an empty ResultSet raises an IndexError exception, where "n/a" is
        # then stored into the corresponding variables.
        ds_home_fact_list_item = ZillowHTML.find_all("li", class_="ds-home-fact-list-item")
        try:
            SoldHomeType = ds_home_fact_list_item[0].text.replace("Type:", "")
        except IndexError:
            SoldHomeType = "n/a"
        try:
            SoldHomeYearBuilt = ds_home_fact_list_item[1].text.replace("Year built:", "")
        except IndexError:
            SoldHomeYearBuilt = "n/a"
        try:
            SoldHomeHeating = ds_home_fact_list_item[2].text.replace("Heating:", "")
        except IndexError:
            SoldHomeHeating = "n/a"
        try:
            SoldHomeCooling = ds_home_fact_list_item[3].text.replace("Cooling:", "")
        except IndexError:
            SoldHomeCooling = "n/a"
        try:
            SoldHomeParking = ds_home_fact_list_item[4].text.replace("Parking:", "")
        except IndexError:
            SoldHomeParking = "n/a"
        try:
            SoldHomeLotSize = ds_home_fact_list_item[5].text.replace("Lot:", "").replace(",", "")
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
