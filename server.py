from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
import pyrebase

config = {
  "apiKey": "AIzaSyBNLdPrHLEnvFJUOTSrAOnvwj9yA6D0WAo",
  "authDomain": "nuitdelinfo2017-4ba50.firebaseapp.com",
  "databaseURL": "https://nuitdelinfo2017-4ba50.firebaseio.com",
  "storageBucket": "nuitdelinfo2017-4ba50.appspot.com",
  "serviceAccount": "firebaseKey.json"
}

firebase = pyrebase.initialize_app(config)
# Get a reference to the database service
db = firebase.database()
# Get a reference to the auth service
# auth = firebase.auth()

app = FlaskAPI(__name__)

users = {
    0: {
        "gpsX": 5,
        "gpsY": 10,
        "matchedWith": 0,
    },
    1: {
        "gpsX": 5,
        "gpsY": 10,
        "matchedWith": 3,
    },
    2: {
        "gpsX": 5,
        "gpsY": 10,
        "matchedWith": 2,
    },
}


@app.route("/findMatch", methods=['GET'])
def tryFindMatch():
    return False

@app.route("/", methods=['GET', 'POST'])
def notes_list():
    """
    List or create notes.
    """
    if request.method == 'POST':
        gpsX = str(request.data.get('gpsX', ''))
        gpsY = str(request.data.get('gpsY', ''))
        idx = max(users.keys()) + 1
        newUser = {
            "gpsX": gpsX,
            "gpsY": gpsY,
            "matchedWith": 0,
        },
        results = db.child("users/"+request.data.get('userId', '')).set(newUser)

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