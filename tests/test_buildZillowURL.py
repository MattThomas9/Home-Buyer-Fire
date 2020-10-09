from src.hbf.buildZillowURL import buildZillowURL
from nose.tools import assert_equal


# Test supporting `getAllSoldHomeZillowURLs.py` functionality.


def test_buildZillowURL():
    obs = buildZillowURL(
        "Recently Sold",
        None,
        39.04860820941063,
        39.04570892556861,
        -77.06767891229457,
        -77.07139696932713,
    )
    exp = "https://www.zillow.com/homes/recently_sold/?searchQueryState={pagination:{},mapBounds:{west:-77.07139696932713,east:-77.06767891229457,south:39.04570892556861,north:39.04860820941063},isMapVisible:true,mapZoom:8,filterState:{isForSaleByAgent:{value:false},isForSaleByOwner:{value:false},isNewConstruction:{value:false},isForSaleForeclosure:{value:false},isComingSoon:{value:false},isAuction:{value:false},isPreMarketForeclosure:{value:false},isPreMarketPreForeclosure:{value:false},isMakeMeMove:{value:false},isRecentlySold:{value:true}},isListVisible:true}"
    assert_equal(exp, obs)
