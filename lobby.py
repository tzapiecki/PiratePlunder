"""
Lobby class to keep information about each game session

Written by Gabriel Brown
"""
from player import Player
import events

class Lobby:

    def __init__(self, lobby_id):
        """Constructor for Lobby"""

        self.lobby_id = lobby_id
        self.numPlayers = 0
        self.numReadyPlayers = 0

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

    def is_ready(self):
        """Returns true if every player is ready and there are at least two players"""

        #return len(self.players) == self.numReadyPlayers and len(self.players) >= 2
        return self.numPlayers >= 2 and self.numPlayers == self.numReadyPlayers

