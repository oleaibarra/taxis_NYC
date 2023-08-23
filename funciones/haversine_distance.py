from math import sin, cos, sqrt, atan2, radians

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371000 # radio de la Tierra en metros
    phi1 = radians(lat1)
    phi2 = radians(lat2)
    delta_phi = radians(lat2 - lat1)
    delta_lambda = radians(lon2 - lon1)

    a = sin(delta_phi / 2)**2 + cos(phi1) * cos(phi2) * sin(delta_lambda / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c