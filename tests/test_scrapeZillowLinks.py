from scrapeZillowLinks import scrapeZillowLinks
from nose.tools import assert_equal


def test_scrapeZillowLinks():
    obs = scrapeZillowLinks(
        [
            "https://www.zillow.com/homedetails/11705-College-View-Dr-Silver-Spring-MD-20902/37316339_zpid/"
        ],
        {
            "accept": "/",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
        },
    )
    exp = [
        [
            "11705 College View Dr Silver Spring MD 20902",
            "293000",
            "2",
            "2",
            "1526 SqFt",
            "Single Family",
            "1951",
            "Forced air",
            "Central",
            "No Data",
            "6791 sqft",
        ]
    ]
    assert_equal(exp, obs)
