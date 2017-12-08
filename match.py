import googlemaps
import json

gmaps = googlemaps.Client(key='AIzaSyAd5jWtKXCH5yt3meKpm7HKKToff4zGR4g')

def matching(origin_user, dest_user, list_users, delta=25):

    duree_min = 9999999
    bourre_a_ramene = None

    for bourre in list_users:
        origins = [origin_user, list_users[bourre]["origin"], list_users[bourre]["destination"]]

        destinations = [dest_user, list_users[bourre]["origin"], list_users[bourre]["destination"]]

        matrix = gmaps.distance_matrix(origins, destinations)

        try:
            duree_initiale = matrix["rows"][0]["elements"][0]["duration"]["value"]
            duree_initiale = int(duree_initiale/60)

            duree_finale = int(matrix["rows"][0]["elements"][1]["duration"]["value"]) \
                    + int(matrix["rows"][1]["elements"][2]["duration"]["value"]) \
                    + int(matrix["rows"][2]["elements"][0]["duration"]["value"])
            duree_finale = int(duree_finale/60)

            if duree_finale-duree_initiale <= delta:
                if duree_finale < duree_min:
                    duree_min = duree_finale
                    bourre_a_ramene = bourre
        except KeyError:
            pass

    if bourre_a_ramene != None:
        return list_users[bourre_a_ramene]
    else:
        return False