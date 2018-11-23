from flask import Flask, render_template, make_response, jsonify, request
from flask_socketio import SocketIO, emit

app = Flask(__name__, static_url_path='')
# TODO: may need to add secret key
socketio = SocketIO(app)


"""
Routes to new pages
"""
@app.route('/')
def index():
    return app.send_static_file('login.html')

@app.route('/lobby/<lobby_id>')
def lobby(lobby_id):

    # If player is sending a status update
    if request.method == 'POST':

        status = request.args.get("status", "none")

        if status == "ready":

            # TODO: update lobby object and emit a socket.io event to  
            # tell all players to load the game page if
            # there are 2+ players in the lobby and all are ready

            # this is here to make everything compile even though we have no implementation yet
            makePythonCompile = True 

        elif status == "unready":

            # TODO: update lobby object
            
            # this is here to make everything compile even though we have no implementation yet
            makePythonCompile = True 


    # If loading lobby page for first time
    else:
        return render_template("lobby.html", lobby_id=lobby_id)

@app.route('/game/<lobby_id>')
def game(lobby_id):

    return render_template("game.html", lobby_id=lobby_id)


"""
Routes to pass around information
"""
@app.route('/game/<lobby_id>/failed/<task_id>')
def task_failed(lobby_id, task_id):

    # TODO: emit a socket.io event that tells each user that a task
    # was failed (and to damage the ship, etc etc)

    # TODO: generate a new task and return that as a json response
    # (the user who failed the task should send the request to this URL,
    # and therefore should get this response)

    return make_response()

@app.route('/game/<lobby_id>/input/<action_id>')
def handle_input(lobby_id, action_id):

    # TODO: check if the input successfully completed a task. 

    # If it did complete a task, emit a socket.io event to that effect
    # and return a json object with a new task and a boolean indicating
    # the action was successful

    # If the action did not complete a task, simply send back false in JSON response
    # NOTE: If we decide to punish this action, then update the ship health and 
    # emit an event to all players to let them know that the ship took damage before
    # sending response

    return make_response()


if __name__ == '__main__':

    print("\n * App running with SocketIO")
    print(" * Should be accessible on http://127.0.0.1:5000\n")
    socketio.run(app)






