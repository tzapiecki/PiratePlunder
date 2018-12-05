"""
Game Lobby class to keep information about each player in a game

Written by Trevor Zapiecki
"""

from .player import Player
from . import events
from .task_generator import TaskGenerator

class GameLobby:
    def __init__(self, lobby_id, numPlayers):
        """Constructor for Lobby"""

        self.lobby_id = lobby_id
        self.numPlayers = numPlayers
        self.connectedPlayers = 0
        self.players = {}       # KEY: user_id/cookies, VALUE: Player object
        self.initial_task_assignments = {} # KEY: user/id cookie, VALUE: task

    def add_player(self, player):
        self.players[player.user_id] = player

    def create_tasks(self):
        self.task_generator = TaskGenerator(len(self.players))

        # Assign tasks
        player_cookies = list(self.players.keys())
        initial_task_ids = list(self.task_generator.current_tasks.keys())

        # Assign tasks in no particular order, just however the dictionaries organize their keys
        for i in range(len(player_cookies)):
            player_cookie = player_cookies[i]
            task_id = initial_task_ids[i]

            self.initial_task_assignments[player_cookie] = self.task_generator.current_tasks[task_id]
