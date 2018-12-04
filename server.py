"""
A flask server that emits asynchronous events to clients
using SocketIO

Written by Gabriel Brown
"""
import json

from flask import Flask, render_template, make_response, request
from flask_socketio import SocketIO, emit

import events
from lobby import Lobby
from player import Player

app = Flask(__name__, static_url_path='')
# TODO: may need to add secret key
socketio = SocketIO(app, ping_interval=1, ping_timeout=3)

"""
Global variables
"""
lobbies = {}   # Key: lobby_id, Value: lobby object
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

        #user_id = request.cookies.get("user_id", "no_user_id")
        status = request.args.get("status", "none")

        print("\n==============\n LOBBY UPDATE \n==============\n")

        lobby = lobbies[lobby_id]

        if status == "ready":

            # update lobby object and emit a socket.io event to  
            # tell all players to load the game page if
            # there are 2+ players in the lobby and all are ready

            #lobby.set_ready(user_id, True)
            lobby.numReadyPlayers += 1
            print(str(lobby) + "\n")

            if lobby.check_ready():

                print("\n==============\n GAME STARTED \n==============\n")
                socketio.emit(events.GAME_START)

            socketio.emit(
                events.LOBBY_STATUS_CHANGED,
                {"numPlayers": lobby.numPlayers, "numReadyPlayers": lobby.numReadyPlayers},
                namespace="/" + lobby_id
            )

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

        lobby = lobbies.get(lobby_id, "no_lobby")

        # If no lobby object with that id found, make a new one
        if(lobby == "no_lobby"):

            lobby = Lobby(lobby_id)
            lobbies[lobby_id] = lobby

            print("\n================\n NEW LOBBY MADE \n================\n")

        # Otherwise update the existing lobby
        else:

            # TODO: make it so that refreshing the page doesn't add new players to the lobby
            # probably easiest to do with cookies. Not important for MVP, but would be good to do later
            pass

        # # Setup cookies
        # user_id = request.cookies.get('user_id', "")

        # # if somehow first page didn't add cookies
        # player = None
        # if user_id == "":
        #     player = Player()   # make new player obj with randomnly generated uuid as user_id

        # # if they have user_id, try and add to lobby
        # else:
        #     player = Player(user_id)
        
        # lobby.add_player(player)


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
        
        # setup response
        response = make_response(render_template("lobby.html", lobby_id=lobby_id, num_players=lobby.numPlayers))
        #response.set_cookie("user_id", player.user_id)

        # # setup response so we can add cookies to it later
        # response = make_response(render_template("lobby.html", lobby_id=lobby_id))


        # # Setup cookies
        # user_id = request.cookies.get('user_id', "")

        # # if user hasn't played pirate plunder before
        # if user_id == "":

        #     player = Player()   # make new player obj with randomnly generated uuid as user_id
        #     response.set_cookie("user_id", player.user_id)
        #     player_added = lobby.add_player(player)

        # # if they have user_id, try and add to lobby
        # else:
        #     player = Player(user_id) 
        #     player_added = lobby.add_player(player)


        # # only print message about player joining if player was actually added (not in lobby before)
        # if player_added:
        #     print("\n===================\n NEW PLAYER JOINED \n===================\n")

        # print(str(lobby) + "\n")

        # TODO: may want to randomly choose a task_id here and now, and save it to tasks

        return response

@app.route('/game/<lobby_id>')
def game(lobby_id):

    lobby = lobbies[lobby_id]
    initial_task = lobby.initial_task_assignments[request.cookies["user_id"]].serialize()

    return render_template("game.html", lobby_id=lobby_id, initial_task=initial_task)


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






