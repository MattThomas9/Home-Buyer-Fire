from preprocess.buildsearchbox import buildsearchbox
from nose.tools import assert_equal


def test_buildsearchbox():
    obs = buildsearchbox("11714 College View Drive   Maryland 20902", 0.1)
    exp = (39.04358264299299, 39.04068335664569, -77.0629061031978, -77.06662389680218)
    assert_equal(exp, obs)
