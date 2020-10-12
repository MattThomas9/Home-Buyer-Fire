from rescrape.getHTML import getHTML
from rescrape.getNumZillowPages import getNumZillowPages
from nose.tools import assert_equal


# Test supporting `getAllSoldHomeZillowURLs.py` functionality.


def test_getNumZillowPages():
    # This test is essentially an integration test as it tests the functionality
    # of `getHTML` to obtain a valid parsable HTML file from Zillow, then checks
    # whether or not `getNumZillowPages` returns the expected number of pages,
    # which is 1 in this case. Note that testing of `getHTML` directly is
    # tricky, and therefore not done directly, since it returns time-dependent
    # data making it impossible to define a static reference result.
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
    obs = getNumZillowPages(getHTMLtest)
    # The fragile logic here is that only 1 page of results will be returned
    # for the test case with such a small search box half width (i.e., 0.1).
    # May need to make this test more robust in future if too fragile.
    exp = 1
    assert_equal(exp, obs)
