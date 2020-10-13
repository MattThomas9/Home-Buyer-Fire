from helpers.logger import logToFile
import numpy as np


def laundry(dirtyLaundry):
    # loop over each row in the data frame for cleaning
    for i, row in dirtyLaundry.iterrows():
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
                dirtyLaundry.loc[i, j] = np.nan
                continue
            # remove the "sqft" string from each item that contains "sqft", then continue to next loop iteration
            if "sqft" in col.lower():
                # first split the item into a list that contains the value and the string
                col = col.lower().split()
                # then remove the item in the new list that matches "sqft"
                col.remove("sqft")
                # store the remaining item from the new size1 list (i.e. the value itself) into the original df location
                dirtyLaundry.loc[i, j] = float(col[0])
                continue
            # remove the "acres" string from each item that contains "acres" and convert to sqft, then continue to next
            # loop iteration
            if "acres" in col.lower():
                # first split the item into a list that contains the value and the string
                col = col.lower().split()
                # then remove the item in the new list that matches "acres"
                col.remove("acres")
                # store the remaining item from the new size1 list (i.e. the value itself) into the original df location
                dirtyLaundry.loc[i, j] = float(col[0]) * 43560.0
                continue

    # convert Sell Price, Beds, Baths, Home Size, Year Built, and Lot Size columns into float type
    dirtyLaundry["Sell Price"] = dirtyLaundry["Sell Price"].astype(float)
    dirtyLaundry["Beds"] = dirtyLaundry["Beds"].astype(float)
    dirtyLaundry["Baths"] = dirtyLaundry["Baths"].astype(float)
    dirtyLaundry["Home Size"] = dirtyLaundry["Home Size"].astype(float)
    dirtyLaundry["Year Built"] = dirtyLaundry["Year Built"].astype(float)
    dirtyLaundry["Lot Size"] = dirtyLaundry["Lot Size"].astype(float)

    # Log clean SoldHomeData
    logToFile(__name__, dirtyLaundry, "INFO")
    # Log clean SoldHomeData datatypes
    logToFile(__name__, dirtyLaundry.dtypes, "INFO")

    print(dirtyLaundry)
    print()

    return
