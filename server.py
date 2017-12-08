from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from test import matching
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
    userData = users[userId]

    pendingSams = {}
    pendingDrunks = {}

    for k, user in users.items():
        if user[0]["pendingSam"] == 'True':
            pendingSams[k] = user[0]

        if user[0]["pendingSam"]  == 'True':
            pendingDrunks[k] = user[0]

    print(matching(userData[0]["origin"], userData[0]["destination"], pendingDrunks))
    return pendingSams, status.HTTP_201_CREATED

@app.route("/", methods=['GET', 'POST'])
def notes_list():
    """
    List or create notes.
    """
    if request.method == 'POST':
        userId = request.data.get('userId', '')
        pendingSam = request.data.get('pendingSam', '')
        matchedWith = request.data.get('matchedWith', '')
        origin = request.data["origin"]
        destination = request.data["destination"]
        newUser = {
            "pendingSam": pendingSam,
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