from scrape.scrapezillowdata import scrapezillowdata
import pandas as pd
from nose.tools import assert_equal


def test_scrapezillowdata():
    obs = scrapezillowdata(
        [
            "https://www.zillow.com/homedetails/11705-College-View-Dr-Silver-Spring-MD-20902/37316339_zpid/"
        ],
        {
            "accept": "/",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/85.0.4183.102 "
            "Safari/537.36",
        },
    )
    exp = pd.DataFrame(
        [
            [
                "11705 College View Dr Silver Spring MD 20902",
                "293000",
                "2",
                "2",
                "1526 sqft",
                "Single Family",
                "1951",
                "Forced air",
                "Central",
                "Garage",
                "6791 sqft",
            ]
        ],
        columns=[
            "Address",
            "Sell Price",
            "Beds",
            "Baths",
            "Home Size",
            "Home Type",
            "Year Built",
            "Heating",
            "Cooling",
            "Parking",
            "Lot Size",
        ],
    )
    assert_equal(exp.values.tolist(), obs.values.tolist())
