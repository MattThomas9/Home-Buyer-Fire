import configparser


def getinput(inp):
    # Read the input file.
    config = configparser.ConfigParser()
    config.read(inp)
    street_number = config.get("Address Control", "Street Number")
    street_name = config.get("Address Control", "Street Name")
    apt_number = config.get("Address Control", "Apartment Number")
    city = config.get("Address Control", "City")
    state = config.get("Address Control", "State")
    zip_code = config.get("Address Control", "Zip Code")
    search_box_half_width = config.getfloat(
        "Search Control", "Search Box Half-Width (miles)"
    )
    zillow_max_result = config.getint("Zillow Control", "Max Result")
    zillow_req_headers = {
        "accept": config.get("Zillow Control", "accept"),
        "accept-encoding": config.get("Zillow Control", "accept-encoding"),
        "accept-language": config.get("Zillow Control", "accept-language"),
        "upgrade-insecure-requests": config.get(
            "Zillow Control", "upgrade-insecure-requests"
        ),
        "user-agent": config.get("Zillow Control", "user-agent").replace("\n", " "),
    }

    return (
        street_number,
        street_name,
        apt_number,
        city,
        state,
        zip_code,
        search_box_half_width,
        zillow_max_result,
        zillow_req_headers,
    )
