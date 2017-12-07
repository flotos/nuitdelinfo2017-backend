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




origin_user = "59 boulevard Jean Brunhes, Toulouse"
dest_user = "Université jean Jaures Toulouse"

list_users = {}
list_users["Bourré 1"] = {}
list_users["Bourré 1"]["origin"] = "2 rue de l'égalité, Toulouse"
list_users["Bourré 1"]["destination"] = "397 route de saint Simon, Toulouse"

list_users["Bourré 2"] = {}
list_users["Bourré 2"]["origin"] = "2 rue de l'égalité, Toulouse"
list_users["Bourré 2"]["destination"] = "395 route de saint Simon, Toulouse"

list_users["Bourré 3"] = {}
list_users["Bourré 3"]["origin"] = (43.5608548, 1.4724762) # = INSA
list_users["Bourré 3"]["destination"] = "395 route de saint Simon, Toulouse"

list_users["Bourré 4"] = {}
list_users["Bourré 4"]["origin"] = (43.012486, -83.6964149) # = Australie
list_users["Bourré 4"]["destination"] = "395 route de saint Simon, Toulouse"

print(matching(origin_user, dest_user, list_users, delta=30))
