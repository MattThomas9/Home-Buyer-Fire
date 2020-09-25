import geopy
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

def getBox(Address, SearchBoxHalfWidth):

    # Nominatim is the GeoCoder class used in this code
    geolocator = Nominatim(user_agent="my_app_rescrape")

    # Using the GeoCoder, we obtain the coordinates of the user supplied address, and if the address cannot be found by
    # the GeoCoder, we prompt the user for a new address. If the Address cannot be found, location
    # is returned as None. When .latitude and .longitude are tried to be executed on a NoneType, the AttributeError is
    # thrown and hence a new address from the user is prompted.
    while True:
        try:
            location = geolocator.geocode(Address)
            origin = geopy.Point(location.latitude, location.longitude)
        except AttributeError:
            print(
                "ERROR!!! The user supplied address cannot be GeoCoded with Nominatim.\n"
                "In some instances, a mailing address is different from its physical address.\n"
                "If this is the case, please try supplying only the street number, name, state, and zip code."
            )
            Address = input(
                "Try typing in the specific physical address using method above: "
            )
            print("Trying to GeoCode the new address: ", Address)
        else:
            print("The address has been GeoCoded!")
            break
    # The search box coordinates are obtained via a geodesic measurement from the origin (e.g. user supplied address) to the
    # direct North, direct East, direct South, and direct West using the user supplied SearchBoxHalfWidth.
    # The North Boundary thus becomes the latitude of the geodesic measurement from the origin, and so on.
    NorthDestination = geodesic(kilometers=(SearchBoxHalfWidth * 1.60934)).destination(
    origin, 0.0
    )
    NorthBoundary = NorthDestination.latitude
    EastDestination = geodesic(kilometers=(SearchBoxHalfWidth * 1.60934)).destination(
    origin, 90.0
    )
    EastBoundary = EastDestination.longitude
    SouthDestination = geodesic(kilometers=(SearchBoxHalfWidth * 1.60934)).destination(
    origin, 180.0
    )
    SouthBoundary = SouthDestination.latitude
    WestDestination = geodesic(kilometers=(SearchBoxHalfWidth * 1.60934)).destination(
    origin, 270.0
    )
    WestBoundary = WestDestination.longitude
    print("Searching within a square area of half-width", SearchBoxHalfWidth, "miles.")

    return NorthBoundary, EastBoundary, SouthBoundary, WestBoundary
