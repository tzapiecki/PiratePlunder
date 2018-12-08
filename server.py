"""
A flask server that emits asynchronous events to clients
using SocketIO

Written by Gabriel Brown and Trevor Zapiecki
"""
import json

from flask import Flask, render_template, make_response, request, redirect
from flask_socketio import SocketIO, emit

from server_classes import events
from server_classes.lobby import Lobby
from server_classes.gameLobby import GameLobby
from server_classes.player import Player

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


            gameLobby.start_game()


            # Serialize initial task assignments
            serializedInitialTasks = {}
            for key in gameLobby.initial_task_assignments.keys():
                task = gameLobby.initial_task_assignments[key]
                serializedInitialTasks[key] = task.serialize()

            # Serialize tasks unique to each user
            serializedUserTasks = {}
            for user_id in gameLobby.user_tasks.keys():

                user_task_list = gameLobby.user_tasks[user_id]
                serialized_list = []
                # If list doesn't work, could assign tasks like task0, task1, etc

                for task in user_task_list:
                    serialized_list.append(task.serialize())

                serializedUserTasks[user_id] = serialized_list


            socketio.emit(
                events.GAME_START,
                {
                    "initialTasks": serializedInitialTasks,
                    "userTasks": serializedUserTasks
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
    """
    Emit a socketio event that tells each user that a task
    was failed, updates the ship and game accordingly,
    and sends a new task to the client that made a call to this route
    """

    socketio.emit(events.TASK_FAILED, { "task_id": task_id }, namespace="/game:" + lobby_id)

    # Generate a new task and return that as a json response
    # (the user who failed the task should send the request to this URL,
    # and therefore should get this response)
    lobby = lobbies[lobby_id]
    new_task = lobby.task_generator.new_task(task_id)

    return make_response( { "new_task": new_task.serialize() } )


@app.route('/game/<lobby_id>/input/<task_id>')
def handle_input(lobby_id, task_id):
    """Check if the input completes one of the currently active tasks"""

    lobby = lobbies[lobby_id]
    current_task_id = lobby.task_generator.current_tasks.get(task_id, "not_current_task")

    # If it did complete a task, emit a socket.io event to that effect
    # and return a json object with a new task
    if task_id != "not_current_task":

        new_task = lobby.task_generator.new_task(current_task_id)
        response_json = { "completed_task_id": current_task_id, "new_task": new_task.serialize() }

        socketio.emit(events.TASK_COMPLETE, response_json, namespace="/game:" + lobby_id)


    # If the action did not complete one of the current tasks, let every client 
    # know that there was bad input. 
    else:

        # TODO: If we want to punish this, we should also reduce the ship health and
        # check for a loss condition
        socketio.emit(events.BAD_INPUT, { "task_id": task_id }, namespace="/game:" + lobby_id)

    return make_response()


if __name__ == '__main__':

    # Uncomment the lines below when not running with debug mode,
    # so you can at least get some feedback that the app has started
    # print("\n * App running with SocketIO")
    # print(" * Should be accessible on http://127.0.0.1:5000\n")

    socketio.run(app, debug=True)






