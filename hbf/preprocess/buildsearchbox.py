from hbf.helpers.logtofile import logtofile
import geopy
from geopy.geocoders import Nominatim
from geopy.distance import geodesic


def buildsearchbox(address, search_box_half_width):

    # Nominatim is the GeoCoder class used in this code
    geolocator = Nominatim(user_agent="hbf")

    # Using the GeoCoder, we obtain the coordinates of the user supplied address, and if the address cannot be found by
    # the GeoCoder, we prompt the user for a new address. If the address cannot be found, location
    # is returned as None. When .latitude and .longitude are tried to be executed on a NoneType, the AttributeError is
    # thrown and hence a new address from the user is prompted.
    while True:
        try:
            location = geolocator.geocode(address)
            origin = geopy.Point(location.latitude, location.longitude)
        except AttributeError:
            print(
                "ERROR!!! The user supplied address cannot be GeoCoded with Nominatim.\n"
                "In some instances, a mailing address is different from its physical address.\n"
                "If this is the case, please try supplying only the street number, name, state, and zip code."
            )
            address = input(
                "Try typing in the specific physical address using method above: "
            )
            print("Trying to GeoCode the new address: ", address)
        else:
            logtofile(__name__, "The address has been GeoCoded!", "INFO")
            break
    mess = "The geocoded origin of the address is: " + str(repr(origin))
    logtofile(__name__, mess, "INFO")
    # The search box coordinates are obtained via a geodesic measurement from the origin (e.g. user supplied address)
    # to the direct North, direct East, direct South, and direct West using the user supplied search_box_half_width.
    # The North Boundary thus becomes the latitude of the geodesic measurement from the origin, and so on.
    north_destination = geodesic(
        kilometers=(search_box_half_width * 1.60934)
    ).destination(origin, 0.0)
    north_boundary = north_destination.latitude
    east_destination = geodesic(
        kilometers=(search_box_half_width * 1.60934)
    ).destination(origin, 90.0)
    east_boundary = east_destination.longitude
    south_destination = geodesic(
        kilometers=(search_box_half_width * 1.60934)
    ).destination(origin, 180.0)
    south_boundary = south_destination.latitude
    west_destination = geodesic(
        kilometers=(search_box_half_width * 1.60934)
    ).destination(origin, 270.0)
    west_boundary = west_destination.longitude

    mess = (
        "Searching within a square area of half-width "
        + str(search_box_half_width)
        + " miles."
    )
    logtofile(__name__, mess, "INFO")

    return north_boundary, south_boundary, east_boundary, west_boundary
