from rescrape.getHTML import getHTML
from rescrape.getNumZillowResults import getNumZillowResults
from nose.tools import assert_equal


# Test supporting `getzillowurls.py` functionality.


def test_getNumZillowResults():
    # This test is essentially an integration test as it tests the functionality
    # of `gethtml` to obtain a valid parsable HTML file from Zillow, then checks
    # whether or not `scraperesultcount` returns the expected number of
    # results. Note that testing of `gethtml` directly is tricky, and therefore
    # not done directly, since it returns time-dependent data making it
    # impossible to define a static reference result.
    getHTMLtest = getHTML(
        "https://www.zillow.com/homes/recently_sold/?searchQueryState={pagination:{},mapBounds:{west:-77.07139696932713,east:-77.06767891229457,south:39.04570892556861,north:39.04860820941063},isMapVisible:true,mapZoom:8,filterState:{isForSaleByAgent:{value:false},isForSaleByOwner:{value:false},isNewConstruction:{value:false},isForSaleForeclosure:{value:false},isComingSoon:{value:false},isAuction:{value:false},isPreMarketForeclosure:{value:false},isPreMarketPreForeclosure:{value:false},isMakeMeMove:{value:false},isRecentlySold:{value:true}},isListVisible:true}",
        {
            "accept": "/",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
        },
    )
    obs = isinstance(getNumZillowResults(getHTMLtest), int)
    # Since the number of results is likely to vary with time, simply check
    # that the returned result is an integer.
    exp = True
    assert_equal(exp, obs)
