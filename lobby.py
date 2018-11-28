"""
Lobby class to keep information about each game session
"""

class Lobby:

    def __init__(self, lobby_id):
        """Constructor for Lobby"""

        self.lobby_id = lobby_id
        self.numPlayers = 0
        self.numReadyPlayers = 0


    def add_player(self):

        self.numPlayers += 1


    def add_ready_player(self):

        self.numReadyPlayers += 1


    def remove_ready_player(self):

        self.numReadyPlayers -= 1
        

    def is_ready(self):
        """Returns true if every player is ready and there are at least two players"""

        return self.numPlayers == self.numReadyPlayers and self.numPlayers == 2

