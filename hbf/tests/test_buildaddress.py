from preprocess.getinput import getinput
from preprocess.buildaddress import buildaddress
from nose.tools import assert_equal


def test_buildaddress():
    (
        street_number,
        street_name,
        apt_number,
        city,
        state,
        zip_code,
        search_box_half_width,
        zillow_max_result,
        zillow_req_headers,
    ) = getinput("./hbf/tests/hbf.inp")
    obs = buildaddress(street_number, street_name, apt_number, city, state, zip_code)
    exp = "11714 College View Drive   Maryland 20902"
    assert_equal(exp, obs)
