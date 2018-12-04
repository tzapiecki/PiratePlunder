"""
Lobby class to keep information about each game session

Written by Gabriel Brown
"""
from player import Player
import events
from task_generator import TaskGenerator

class Lobby:

    def __init__(self, lobby_id):
        """Constructor for Lobby"""

        self.lobby_id = lobby_id
        self.numPlayers = 0
        self.players = {}       # KEY: user_id/cookies, VALUE: Player object
        self.numReadyPlayers = 0
        self.initial_task_assignments = {} # KEY: user/id cookie, VALUE: task

    def __str__(self):
        """Prints out info about lobby"""

        return "Lobby_id: " + self.lobby_id + "\nNum players: " + str(self.numPlayers) + "\nNum ready players: " + str(self.numReadyPlayers)


    def player_is_in_lobby(self, user_id):
        """Returns true if player with that user_id is already in the lobby"""

        return self.players.get(user_id, "no_player") != "no_player"


    def add_player(self):
        """Adds the player object passed in provided they're not already in lobby"""
        self.numPlayers += 1

    def remove_player(self):
        self.numPlayers -= 1
    def add_player(self, player):
        """
        Adds the player object passed in provided they're not already in lobby.
        Returns a boolean that is true if player needed to be added to lobby
        """

        if not self.player_is_in_lobby(player.user_id):

            self.players[player.user_id] = player
            return True

        else:
            
            return False


    def toggle_ready(self, user_id):
        """
        Toggles the given player's ready status and updates numReadyPlayers accordingly,
        assuming they were in the lobby to begin with
        """

        if self.player_is_in_lobby(user_id):

            player = self.players[user_id]

            new_ready_status = not player.ready # save to update numReadyPlayers later
            player.ready = new_ready_status     # update player object in this lobby

            if new_ready_status:
                self.numReadyPlayers += 1

            else:
                self.numReadyPlayers -= 1
    
    def set_ready(self, user_id, ready_status):
        """
        Sets the player's ready status to the given value, and updates the number of ready
        players if the status has changed, assuming they were in the lobby to begin with
        """

        if self.player_is_in_lobby(user_id):

            player = self.players[user_id]

            if player.ready != ready_status:

                player.ready = ready_status

                if ready_status:
                    self.numReadyPlayers += 1
                    
                else:
                    self.numReadyPlayers -= 1

    def check_ready(self):
        """
        If every player is ready and there are at least two players,
        returns true and sets up task generator and initial tasks
        """

        if len(self.players) == self.numReadyPlayers and len(self.players) >= 2:

            self.task_generator = TaskGenerator(len(self.players))

            # Assign tasks
            player_cookies = list(self.players.keys())
            initial_task_ids = self.task_generator.current_tasks.keys()

            # Assign tasks in no particular order, just however the dictionaries organize their keys
            for i in range(len(player_cookies)):

                player_cookie = player_cookies[i]
                task_id = initial_task_ids[i]

                self.initial_task_assignments[player_cookie] = self.task_generator.current_tasks[task_id]

            return True

        else:
            return False

        #return len(self.players) == self.numReadyPlayers and len(self.players) >= 2
        return self.numPlayers >= 2 and self.numPlayers == self.numReadyPlayers