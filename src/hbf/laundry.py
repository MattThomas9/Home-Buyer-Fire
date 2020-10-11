

def laundry(dirtyLaundry):
    # remove "SqFt" and "sqft" unit labels
    # dirtyLaundry = dirtyLaundry.replace({'SqFt': '', 'sqft': ''}, regex=True)

    # change Sell Price, Beds, Baths, and Home Size columns into float type
    # dirtyLaundry['Sell Price'] = dirtyLaundry['Sell Price'].astype(float)
    # dirtyLaundry['Beds'] = dirtyLaundry['Beds'].astype(float)
    # dirtyLaundry['Baths'] = dirtyLaundry['Baths'].astype(float)
    # dirtyLaundry['Home Size'] = dirtyLaundry['Home Size'].astype(float)

    # change Year Built column into integer type
    # dirtyLaundry['Year Built'] = dirtyLaundry['Year Built'].astype(int)

    # loop over each row in the data frame
    for i, row in dirtyLaundry.iterrows():

        # remove 'sqft' string from current row in column 'Lot Size'
        if 'sqft' in row['Lot Size']:  # said as: if 'sqft' is in the current row of column 'Lot Size'

            # first, split the current element into a list that contains the lot size value and the 'sqft' string
            lotSize = row['Lot Size'].split()

            # next, remove the string 'sqft' from the list
            lotSize.remove('sqft')

            # next, convert the leftover string value to a float
            lotSize = list(map(float, lotSize))

            # finally, replace the original dataframe element with new value
            dirtyLaundry.at[i, 'Lot Size'] = lotSize[0]

        # remove 'Acres' string from current row in column 'Lot Size'
        elif 'Acres' in row['Lot Size']:  # said as: if 'Acres' is in the current row of column 'Lot Size'

            # first, split the current element into a list that contains the lot size value and the 'Acres' string
            lotSize = row['Lot Size'].split()

            # next, remove the string 'Acres' from the list
            lotSize.remove('Acres')

            # next, convert the leftover string value to a float
            lotSize = list(map(float, lotSize))

            # next, convert Acres into Square Feet
            lotSize[0] = lotSize[0] * 43560.0

            # finally, replace the original dataframe element with new value
            dirtyLaundry.at[i, 'Lot Size'] = lotSize[0]

    print(dirtyLaundry)
    return
