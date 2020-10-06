import configparser
from src.getAddress import getAddress
from nose.tools import assert_equal

def test_getAddress():
    obs = getAddress("res.inp")
    exp = ('11714 College View Drive   Maryland 20902', 0.1)
    assert_equal(exp, obs)
