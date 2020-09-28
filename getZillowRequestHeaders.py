import configparser


def getZillowRequestHeaders():
    # Read the input file for Zillow specific inputs.
    config = configparser.ConfigParser()
    config.read("res.inp")
    req_headers = {
        "accept": config.get("Zillow Control", 'accept'),
        "accept-encoding": config.get("Zillow Control", 'accept-encoding'),
        "accept-language": config.get("Zillow Control", 'accept-language'),
        "upgrade-insecure-requests": config.get("Zillow Control", 'upgrade-insecure-requests'),
        "user-agent": config.get("Zillow Control", 'user-agent').replace('\n', ' ')
    }
    return req_headers
