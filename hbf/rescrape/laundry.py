import numpy as np


def laundry(dirtyLaundry):

    # first replace all values in data frame with NaN where "n/a" or "No Data" or "--" exists
    dirtyLaundry = dirtyLaundry.where(
        (dirtyLaundry != "n/a") & (dirtyLaundry != "No Data") & (dirtyLaundry != "--"),
        np.nan,
    )
    # loop over each row in the data frame and clean
    for i, row in dirtyLaundry.iterrows():
        # remove 'SqFt' string from current row in column 'Home Size'
        if row["Home Size"].isnull():
            continue
        elif "SqFt" in row["Home Size"]:
            # first, split the current element into a list that contains the home size value and the 'SqFt' string
            homeSize = row["Home Size"].split()
            # next, remove the string 'SqFt' from the list
            homeSize.remove("SqFt")
            # next, convert the leftover string value to a float
            homeSize = list(map(float, homeSize))
            # finally, replace the original dataframe element with new value
            dirtyLaundry.at[i, "Home Size"] = homeSize[0]
        # remove 'sqft' string from current row in column 'Lot Size'
        print("i: ", i, " row[lot size]: ", row["Lot Size"])
        if row[
            "Lot Size"
        ].isnull():  # UGH NEED TO FIX THIS............................................................
            print("yeet")
            continue
        elif (
            "sqft" in row["Lot Size"]
        ):  # said as: if 'sqft' is in the current row of column 'Lot Size'
            # first, split the current element into a list that contains the lot size value and the 'sqft' string
            lotSize = row["Lot Size"].split()
            # next, remove the string 'sqft' from the list
            lotSize.remove("sqft")
            # next, convert the leftover string value to a float
            lotSize = list(map(float, lotSize))
            # finally, replace the original dataframe element with new value
            dirtyLaundry.at[i, "Lot Size"] = lotSize[0]
        # remove 'Acres' string from current row in column 'Lot Size'
        elif (
            "Acres" in row["Lot Size"]
        ):  # said as: if 'Acres' is in the current row of column 'Lot Size'
            # first, split the current element into a list that contains the lot size value and the 'Acres' string
            lotSize = row["Lot Size"].split()
            # next, remove the string 'Acres' from the list
            lotSize.remove("Acres")
            # next, convert the leftover string value to a float
            lotSize = list(map(float, lotSize))
            # next, convert Acres into Square Feet
            lotSize[0] = lotSize[0] * 43560.0
            # finally, replace the original dataframe element with new value
            dirtyLaundry.at[i, "Lot Size"] = lotSize[0]
    # convert Sell Price, Beds, Baths, Home Size, and Lot Size columns into float type
    dirtyLaundry["Sell Price"] = dirtyLaundry["Sell Price"].astype(float)
    dirtyLaundry["Beds"] = dirtyLaundry["Beds"].astype(float)
    dirtyLaundry["Baths"] = dirtyLaundry["Baths"].astype(float)
    dirtyLaundry["Home Size"] = dirtyLaundry["Home Size"].astype(float)
    dirtyLaundry["Lot Size"] = dirtyLaundry["Lot Size"].astype(float)

    # change Year Built column into integer type
    dirtyLaundry["Year Built"] = dirtyLaundry["Year Built"].astype(int)

    print(dirtyLaundry)
    print(dirtyLaundry.dtypes)
    return
