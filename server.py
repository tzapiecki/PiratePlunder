"""
A flask server that emits asynchronous events to clients
using SocketIO

Written by Gabriel Brown
"""
import json

from flask import Flask, render_template, make_response, request, redirect
from flask_socketio import SocketIO, emit

import events
from lobby import Lobby
from gameLobby import GameLobby
from player import Player

app = Flask(__name__, static_url_path='')
# TODO: may need to add secret key

# The ping interval is how often it checks in with clients (1 second)
# The ping timeout is when the server considers a client disconnected (after 3 seconds)
socketio = SocketIO(app, ping_interval=1, ping_timeout=3) 

"""
Global variables
"""
stagingLobbies = {}   # Key: lobby_id, Value: lobby object
gameLobbies = {}
tasks = [] 

"""
Routes to new pages
"""
@app.route('/')
def index():

    return app.send_static_file('login.html')

@app.route('/lobby/<lobby_id>', methods=['GET', 'POST'])
def lobby(lobby_id):

    # If player is sending a status update
    if request.method == 'POST':

        status = request.args.get("status", "none")

        print("\n==============\n LOBBY UPDATE \n==============\n")

        lobby = stagingLobbies[lobby_id]

        if status == "ready":
            lobby.numReadyPlayers += 1
            print(str(lobby) + "\n")

            socketio.emit(
                events.LOBBY_STATUS_CHANGED,
                {"numPlayers": lobby.numPlayers, "numReadyPlayers": lobby.numReadyPlayers},
                namespace="/" + lobby_id
            )

            if lobby.check_ready():
                gameLobbies[lobby_id] = GameLobby(lobby_id, lobby.numPlayers)

                socketio.emit(
                    events.GAME_LOAD,
                    {},
                    namespace="/" + lobby_id
                )
                print("\n==============\n GAME STARTED \n==============\n")

            return make_response()


        elif status == "unready":
            # lobby.set_ready(user_id, False)
            lobby.numReadyPlayers -= 1
            print(str(lobby) + "\n")

            socketio.emit(
                events.LOBBY_STATUS_CHANGED,
                {"numPlayers": lobby.numPlayers, "numReadyPlayers": lobby.numReadyPlayers},
                namespace="/" + lobby_id
            )

            return make_response()


    # If loading the lobby page
    else:
        lobby = stagingLobbies.get(lobby_id, "no_lobby")

        # If no lobby object with that id found, make a new one
        if (lobby == "no_lobby"):

            lobby = Lobby(lobby_id)
            stagingLobbies[lobby_id] = lobby

            print("\n================\n NEW LOBBY MADE \n================\n")

        def playerDisconnected():
            lobby.remove_player()
            lobby.numReadyPlayers = 0
            print("\n===================\n PLAYER DISCONNECTED \n===================\n")
            print(str(lobby))
            socketio.emit(
                events.PLAYER_DISCONNECTED,
                { "numPlayers": lobby.numPlayers, "numReadyPlayers": lobby.numReadyPlayers},
                namespace="/" + lobby_id
            )
        socketio.on_event(
            'disconnect',
            playerDisconnected,
            namespace="/" + lobby_id
        )

        def playerConnected():
            lobby.add_player()
            print("\n===================\n NEW PLAYER CONNECTED \n===================\n")
            print(str(lobby))
            socketio.emit(
                events.PLAYER_JOINED,
                {"numPlayers": lobby.numPlayers, "numReadyPlayers": lobby.numReadyPlayers},
                namespace = "/" + lobby_id
            )
        socketio.on_event(
            'connect',
            playerConnected,
            namespace = "/" + lobby_id
        )
        
        response = make_response(render_template("lobby.html", lobby_id=lobby_id, num_players=lobby.numPlayers))

        return response

@app.route('/game/<lobby_id>')
def game(lobby_id):
    gameLobby = gameLobbies.get(lobby_id, "no_lobby")

    # If no gameLobby object with that id found, redirect to the staging lobby
    if(gameLobby == "no_lobby"):
        return redirect("/lobby/" + lobby_id)

    # Setup cookies
    user_id = request.cookies.get('user_id', "")

    player = None
    # if user hasn't played pirate plunder before
    if user_id == "":
        player = Player()   # make new player obj with randomnly generated uuid as user_id
    else:
        player = Player(user_id)

    gameLobby.add_player(player)

    def playerConnects():
        gameLobby.connectedPlayers += 1
        if gameLobby.connectedPlayers == gameLobby.numPlayers:

            gameLobby.create_tasks()

            serializedTasks = {}
            for key in gameLobby.initial_task_assignments.keys():
                task = gameLobby.initial_task_assignments[key]
                serializedTasks[key] = task.serialize()

            socketio.emit(
                events.GAME_START,
                {
                    "initialTasks": serializedTasks
                },
                namespace="/game:" + lobby_id
            )
    socketio.on_event("connect", playerConnects, namespace="/game:" + lobby_id)

    response = make_response(render_template("game.html", lobby_id=lobby_id, user_id=player.user_id))
    response.set_cookie("user_id", player.user_id)

    return response


"""
Routes to pass around information
"""
@app.route('/game/<lobby_id>/failed/<task_id>')
def task_failed(lobby_id, task_id):

    # emit a socket.io event that tells each user that a task
    # was failed (and to damage the ship, etc etc)

    # When socketio.emit() is used rather than just emit() under
    # a socketio decorater, it's assumed to broadcast to everyone connected

    # Since there could be multiple lobbies at once, I'm including the lobby_id
    # in the data sent with the event so that different lobbies won't get conflicting results
    socketio.emit(events.TASK_FAILED, { "lobby_id": lobby_id, "task_id": task_id })

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

    # TODO: uncomment the lines below when not running with debug mode,
    # so you can at least get some feedback that the app has started
    # print("\n * App running with SocketIO")
    # print(" * Should be accessible on http://127.0.0.1:5000\n")
    socketio.run(app, debug=True)






