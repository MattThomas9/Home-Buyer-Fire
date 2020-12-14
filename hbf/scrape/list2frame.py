from hbf.helpers.logtofile import logtofile
import pandas as pd


def list2frame(data_list):
    data_frame = pd.DataFrame(
        data_list,
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

    # Print data_frame to screen
    pd.set_option(
        "display.max_rows", None, "display.max_columns", None, "display.width", None
    )

    # Log dirty data_frame
    logtofile(__name__, data_frame, "INFO")

    return data_frame
