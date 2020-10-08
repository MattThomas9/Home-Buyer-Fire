from soldHomeDF import soldHomeDF
import pandas as pd
from nose.tools import assert_equal


def test_soldHomeDF():
    obs = soldHomeDF(
        [
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
    )
    exp = pd.DataFrame(
        [
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
