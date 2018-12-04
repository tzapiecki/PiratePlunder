"""
Lobby class to keep information about each players getting ready for game session

Written by Gabriel Brown
"""

class Lobby:

    def __init__(self, lobby_id):
        """Constructor for Lobby"""

        self.lobby_id = lobby_id
        self.numPlayers = 0
        self.numReadyPlayers = 0

    def __str__(self):
        """Prints out info about lobby"""

        return "Lobby_id: " + self.lobby_id + "\nNum players: " + str(self.numPlayers) + "\nNum ready players: " + str(self.numReadyPlayers)

    def add_player(self):
        """Adds the player object passed in provided they're not already in lobby"""
        self.numPlayers += 1

    def remove_player(self):
        self.numPlayers -= 1

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
        returns true
        """

        return self.numPlayers == self.numReadyPlayers and self.numPlayers >= 2