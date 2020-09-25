import configparser

def getAddress(inp):
    # Read the input file.
    config = configparser.ConfigParser()
    config.read(inp)
    StreetNumber = config.get("Address Control", "Street Number")
    StreetName = config.get("Address Control", "Street Name")
    AptNumber = config.get("Address Control", "Apartment Number")
    City = config.get("Address Control", "City")
    State = config.get("Address Control", "State")
    ZipCode = config.get("Address Control", "Zip Code")
    SearchBoxHalfWidth = config.getfloat("Search Control", "Search Box Half-Width (miles)")

    # Construct the Address variable with the input supplied by the user
    Address = (
        StreetNumber
        + " "
        + StreetName
        + " "
        + AptNumber
        + " "
        + City
        + " "
        + State
        + " "
        + ZipCode
    )

    return Address, SearchBoxHalfWidth
