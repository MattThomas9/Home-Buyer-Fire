import configparser


def getInput(inp):
    # Read the input file.
    config = configparser.ConfigParser()
    config.read(inp)
    StreetNumber = config.get("Address Control", "Street Number")
    StreetName = config.get("Address Control", "Street Name")
    AptNumber = config.get("Address Control", "Apartment Number")
    City = config.get("Address Control", "City")
    State = config.get("Address Control", "State")
    ZipCode = config.get("Address Control", "Zip Code")
    SearchBoxHalfWidth = config.getfloat(
        "Search Control", "Search Box Half-Width (miles)"
    )
    RequestHeaders = {
        "accept": config.get("Zillow Control", "accept"),
        "accept-encoding": config.get("Zillow Control", "accept-encoding"),
        "accept-language": config.get("Zillow Control", "accept-language"),
        "upgrade-insecure-requests": config.get(
            "Zillow Control", "upgrade-insecure-requests"
        ),
        "user-agent": config.get("Zillow Control", "user-agent").replace("\n", " "),
    }

    return (
        StreetNumber,
        StreetName,
        AptNumber,
        City,
        State,
        ZipCode,
        SearchBoxHalfWidth,
        RequestHeaders,
    )
