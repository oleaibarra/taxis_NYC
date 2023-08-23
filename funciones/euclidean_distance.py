from math import cos, sqrt

def euclidean_distance(lat1, lon1, lat2, lon2):
    x = (lon2 - lon1) * cos(0.5 * (lat2 + lat1))
    y = lat2 - lat1
    return sqrt(x * x + y * y) * 6371000