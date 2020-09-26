import pandas as pd

def soldHomeDF(SoldHomeDataList):
    SoldHomeData = pd.DataFrame(
        SoldHomeDataList,
        columns=['Address',
                 'Sell Price',
                 'Beds',
                 'Baths',
                 'Home Size',
                 'Home Type',
                 'Year Built',
                 'Heating',
                 'Cooling',
                 'Parking',
                 'Lot Size'
                 ]
    )

    # Print SoldHomeData to screen
    pd.set_option('display.max_rows', None,
                  'display.max_columns', None,
                  'display.width', None)
    print(SoldHomeData)

    return(SoldHomeData)
