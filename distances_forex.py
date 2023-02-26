import geopy.distance


def distance_to_me(lat1, lon1, lat2, lon2):
	return geopy.distance.geodesic((lat1, lon1), (lat2, lon2))


# TODO
# should return a range for quicker db filtering
def latitude_scope(lat, distance_km, multiplier_lat=110):
	print(f"Latitude_scope data:\n"
		  f"lat: {type(lat)}\n"
		  f"distance in km: {type(distance_km)}\n"
		  f"latitude multiplier: {type(multiplier_lat)}")
	print(f"Latitude_scope data:\n"
		  f"lat: {lat}\n"
		  f"distance in km: {distance_km}\n"
		  f"latitude multiplier: {multiplier_lat}")
	min_lat = lat - distance_km / multiplier_lat
	max_lat = lat + distance_km / multiplier_lat
	return min_lat, max_lat


def longitude_scope(lon, distance_km, multiplier_lon=85):
	print(f"Longitude_scope data:\n"
		  f"lon: {lon}\n"
		  f"distance in km: {distance_km}\n"
		  f"longitude multiplier: {multiplier_lon}")
	min_lon = lon - distance_km / multiplier_lon
	max_lon = lon + distance_km / multiplier_lon
	return min_lon, max_lon

# TODO
def optimised_distance_constraints(lat, lon, distance_km):
	pass

# possibly TODO
# if problems arise from locations near the equator and/or greenwich meridian
def equator_fix():
	return


def greenwich_fix():
	return
