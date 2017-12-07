from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions

app = FlaskAPI(__name__)

users = {
    0: {
        "userId": 1,
        "gpsX": 5,
        "gpsY": 10,
        "matchedWith": 0,
    },
    1: {
        "userId": 2,
        "gpsX": 5,
        "gpsY": 10,
        "matchedWith": 3,
    },
    2: {
        "userId": 3,
        "gpsX": 5,
        "gpsY": 10,
        "matchedWith": 2,
    },
}


def users_repr(key):
    return {
        'url': request.host_url.rstrip('/') + url_for('notes_detail', key=key),
        'users': users[key]
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
        users[idx] = {
            "userId": idx,
            "gpsX": gpsX,
            "gpsY": gpsY,
            "matchedWith": 0,
        },
        return users_repr(idx), status.HTTP_201_CREATED

    # request.method == 'GET'
    return [users_repr(idx) for idx in sorted(users.keys())]


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
    if key not in users:
        raise exceptions.NotFound()
    return users_repr(key)


if __name__ == "__main__":
    app.run(debug=True)