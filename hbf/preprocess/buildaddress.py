def buildaddress(street_number, street_name, apt_number, city, state, zip_code):
    address = (
        street_number
        + " "
        + street_name
        + " "
        + apt_number
        + " "
        + city
        + " "
        + state
        + " "
        + zip_code
    )
    return address
