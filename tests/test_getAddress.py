from getInput import getInput
from getAddress import getAddress
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
    ) = getInput("../../tests/res.inp")
    obs = getAddress(StreetNumber, StreetName, AptNumber, City, State, ZipCode)
    exp = "11714 College View Drive   Maryland 20902"
    assert_equal(exp, obs)
