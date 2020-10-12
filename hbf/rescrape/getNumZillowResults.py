def getNumZillowResults(ZillowHTML):
    ZillowResultCount = int(
        (ZillowHTML.find("span", class_="result-count"))
        .text.split()[0]
        .replace(",", "")
    )
    print(
        ZillowResultCount,
        "recently sold homes on Zillow were found within the search box.",
    )
    # Zillow limits the number of pages of a search to 20, and the number of results/page to 40; therefore, the maximum
    # number of results one can obtain is 800.
    if ZillowResultCount > 800:
        print(
            "Warning! The maximum number of pages Zillow shows is 20 and the maximum number of results per page is 40."
        )
        print("Therefore, only 800 recently sold home links will be scraped.")
        ZillowResultCount = 800

    return ZillowResultCount
