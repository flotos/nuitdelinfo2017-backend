from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from match import matching
import pyrebase

config = {
  "apiKey": "AIzaSyBNLdPrHLEnvFJUOTSrAOnvwj9yA6D0WAo",
  "authDomain": "nuitdelinfo2017-4ba50.firebaseapp.com",
  "databaseURL": "https://nuitdelinfo2017-4ba50.firebaseio.com",
  "storageBucket": "nuitdelinfo2017-4ba50.appspot.com",
  "serviceAccount": "firebaseKey.json"
}

# {
#     "userId": "lolilol58",
#     "pendingSam": true,
#     "matchedWith": 0,
#     "origin": {
#         "lat": "10",
#         "lng": "5"
#     },
#     "destination": {
#         "lat": "20",
#         "lng": "25"
#     }
# }

firebase = pyrebase.initialize_app(config)
# Get a reference to the database service
db = firebase.database()
# Get a reference to the auth service
# auth = firebase.auth()

app = FlaskAPI(__name__)

@app.route("/findRoute", methods=['GET'])
def findRoute():
    userId = request.args.get('userId')
    users = db.child("users").get().val()
    # print("users")
    # for i in users:
    #     print (i, users[i])
    userData = users[userId][0]

    pendingSams = {}
    pendingDrunks = {}
    
    requestStatus = ''
    if userData["pendingDrunk"] == 'True':
        requestStatus = "Drunk"
    if userData["pendingSam"] == 'True':
        requestStatus = "Sam"

    for k, user in users.items():
        if requestStatus == "Drunk":
            if user[0]["pendingSam"] == 'True':
                pendingSams[k] = user[0]
        elif requestStatus == "Sam":
            if user[0]["pendingDrunk"]  == 'True':
                pendingDrunks[k] = user[0]

    if requestStatus == "Drunk":
        result = matching(userData["origin"], userData["destination"], pendingSams)
    elif requestStatus == "Sam":
        result = matching(userData["origin"], userData["destination"], pendingDrunks)

    if result is False:
        return {}, status.HTTP_204_NO_CONTENT
    else:
        db.child("users").child(userId).child("0").update({"matchedWith": result["userId"]})
        db.child("users").child(result["userId"]).child("0").update({"matchedWith": userId})
        return result, status.HTTP_201_CREATED

@app.route("/updateTrip", methods=['POST'])
def addTrip():
    userId = request.data.get('userId')
    origin = request.data.get('origin')
    destination = request.data.get('destination')
    result = db.child("users").child(userId).update({"origin": origin, "destination": destination})

    if result is False:
        return {}, status.HTTP_204_NO_CONTENT
    return result, status.HTTP_201_CREATED


@app.route("/", methods=['GET', 'POST'])
def notes_list():
    """
    List or create notes.
    """
    if request.method == 'POST':
        userId = request.data.get('userId', '')
        pendingSam = request.data.get('pendingSam', '')
        pendingDrunk = request.data.get('pendingDrunk', '')
        matchedWith = request.data.get('matchedWith', '')
        origin = request.data["origin"]
        destination = request.data["destination"]
        newUser = {
            "userId": userId,
            "pendingSam": pendingSam,
            "pendingDrunk": pendingDrunk,
            "matchedWith": matchedWith,
            "origin": origin,
            "destination": destination
        },
        results = db.child("users/"+request.data.get('userId')).set(newUser)

        return results, status.HTTP_201_CREATED

    # request.method == 'GET'
    return db.child("users").get().val()


@app.route("/<int:key>/", methods=['GET', 'PUT', 'DELETE'])
def notes_detail(key):
    """
    Retrieve, update or delete note instances.
    """
    # if request.method == 'PUT':
    #     note = str(request.data.get('text', ''))
    #     notes[key] = note
    #     return users_repr(key)

    # elif request.method == 'DELETE':
    #     notes.pop(key, None)
    #     return '', status.HTTP_204_NO_CONTENT

    # request.method == 'GET'
    # if key not in users:
    #     raise exceptions.NotFound()
    # return users_repr(key)


if __name__ == "__main__":
    app.run(debug=True)