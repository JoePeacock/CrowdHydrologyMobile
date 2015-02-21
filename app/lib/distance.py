import math


def find_closest_station(lat, long, station):
    distances = {}
    for s in station.items:
        if s.online:
            theta = s.longitude-long
            dist = math.sin(math.radians(s.latitude)) * math.sin(
                math.radians(lat))+math.cos(math.radians(s.latitude)) * math.cos(
                math.radians(lat)) * math.cos(math.radians(theta))
            dist = math.acos(dist)
            dist = math.degrees(dist)
            miles = dist * 60 * 1.1515
            distances[miles] = s
    l = sorted(distances.keys())
    closest = l[0]
    return distances[closest]


