

def getAddress(StreetNumber, StreetName, AptNumber, City, State, ZipCode):
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

    return Address
