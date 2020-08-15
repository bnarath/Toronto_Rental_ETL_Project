import math
def harvesine_distance(loc1, loc2):
    '''
    input: locations as lat, long
    output: harvesine_distance
    '''
    lat1, long1 = loc1
    lat2, long2 = loc2
    lat1 = lat1*math.pi/180
    lat2 = lat2*math.pi/180
    long1 = long1*math.pi/180
    long2 = long2*math.pi/180
    dlat = (lat2-lat1)
    dlong = (long2-long1)
    R = 6371
    a = math.sin(dlat/2)**2 + (math.cos(lat1)*math.cos(lat2)*math.sin(dlong/2)**2)
    b = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
    c = R*b
    return c