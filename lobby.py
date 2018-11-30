"""
Lobby class to keep information about each game session

Written by Gabriel Brown
"""
from player import Player

class Lobby:

    def __init__(self, lobby_id):
        """Constructor for Lobby"""

        self.lobby_id = lobby_id
        self.players = {}       # KEY: cookie, VALUE: Player object
        self.numReadyPlayers = 0

    def __str__(self):
        """Prints out info about lobby"""

        return "Lobby_id: " + self.lobby_id + "\nNum players: " + str(len(self.players)) + "\nNum ready players: " + str(self.numReadyPlayers)


    def player_is_in_lobby(self, user_id):
        """Returns true if player with that user_id is already in the lobby"""

        return self.players.get(user_id, "no_player") != "no_player"


    def add_player(self, player):
        """Adds the player object passed in provided they're not already in lobby"""

        if not self.player_is_in_lobby(player):

            self.players[player.user_id] = player


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
        

    def is_ready(self):
        """Returns true if every player is ready and there are at least two players"""

        return len(self.players) == self.numReadyPlayers and len(self.players) >= 2

