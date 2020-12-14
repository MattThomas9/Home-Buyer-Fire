from hbf.helpers.logtofile import logtofile
import numpy as np


def laundry(dirty_laundry):
    # loop over each row in the data frame for cleaning
    for i, row in dirty_laundry.iterrows():
        # loop over each column in each row for cleaning
        for j, col in row.iteritems():
            # first convert all "n/a"s, "No Data"s, and "--"s to np.nans, and continue next loop iteration
            if (
                "n/a" in col
                or "No Data" in col
                or "--" in col
                or "Off" in col
                or col == ""
            ):
                dirty_laundry.loc[i, j] = np.nan
                continue
            # remove the "sqft" string from each item that contains "sqft", then continue to next loop iteration
            if "sqft" in col.lower():
                # first split the item into a list that contains the value and the string
                col = col.lower().split()
                # then remove the item in the new list that matches "sqft"
                col.remove("sqft")
                # store the remaining item from the new size1 list (i.e. the value itself) into the original df location
                dirty_laundry.loc[i, j] = float(col[0])
                continue
            # remove the "acres" string from each item that contains "acres" and convert to sqft, then continue to next
            # loop iteration
            if "acres" in col.lower():
                # first split the item into a list that contains the value and the string
                col = col.lower().split()
                # then remove the item in the new list that matches "acres"
                col.remove("acres")
                # store the remaining item from the new size1 list (i.e. the value itself) into the original df location
                dirty_laundry.loc[i, j] = float(col[0]) * 43560.0
                continue

    # convert Sell Price, Beds, Baths, Home Size, Year Built, and Lot Size columns into float type
    dirty_laundry["Sell Price"] = dirty_laundry["Sell Price"].astype(float)
    dirty_laundry["Beds"] = dirty_laundry["Beds"].astype(float)
    dirty_laundry["Baths"] = dirty_laundry["Baths"].astype(float)
    dirty_laundry["Home Size"] = dirty_laundry["Home Size"].astype(float)
    dirty_laundry["Year Built"] = dirty_laundry["Year Built"].astype(float)
    dirty_laundry["Lot Size"] = dirty_laundry["Lot Size"].astype(float)

    # Log cleaned data frame
    logtofile(__name__, dirty_laundry, "INFO")
    # Log cleaned data frame data types
    logtofile(__name__, dirty_laundry.dtypes, "INFO")

    print(dirty_laundry)
    print()
    # return dirty_laundry, which is actually now cleaned
    return dirty_laundry
