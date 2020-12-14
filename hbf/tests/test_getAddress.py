from rescrape.getInput import getInput
from rescrape.getAddress import getAddress
from nose.tools import assert_equal


def test_getAddress():
    (
        StreetNumber,
        StreetName,
        AptNumber,
        City,
        State,
        ZipCode,
        SearchBoxHalfWidth,
        RequestHeaders,
    ) = getInput("./hbf/tests/hbf.inp")
    obs = getAddress(StreetNumber, StreetName, AptNumber, City, State, ZipCode)
    exp = "11714 College View Drive   Maryland 20902"
    assert_equal(exp, obs)
