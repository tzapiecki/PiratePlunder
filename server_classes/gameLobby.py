"""
Game Lobby class to keep information about each player in a game

Written by Trevor Zapiecki and Gabriel Brown
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
        self.players = {}               # KEY: user_id/cookies, VALUE: Player object

        # KEY: user/id cookie, VALUE: first task that user has to complete
        self.initial_task_assignments = {}

        # KEY: userid/cookie, VALUE: a list of tasks that this particular 
        # user can complete (should appear with buttons on their screen)
        self.user_tasks = {}


        self.ship_health = 100          # The overall ship health

        self.task_fail_damage = 10      # The amount of damage failing a task deals to the ship
        self.bad_input_damage = 5       # The amount of damage pressing a the wrong button deals to the ship

        self.num_tasks_to_complete = 5  # The number of tasks players must complete before moving on to a new sector
        self.num_tasks_completed = 0    # The number of tasks players have actually completed

        self.has_won = False
        self.section_complete = False


    def add_player(self, player):
        self.players[player.user_id] = player

    
    def start_game(self):
        """This should be called whenever all the players connect to a game for the first time"""

        self.task_generator = TaskGenerator(len(self.players))
        self.assign_tasks()


    def assign_tasks(self):
        """
        Assign tasks to each player, both the task that they must complete
        as well as the list of tasks that they are able to complete 
        (which buttons should appear on their screen)
        """

        player_cookies = list(self.players.keys())
        initial_task_ids = list(self.task_generator.current_tasks.keys())
        usable_task_ids = list(self.task_generator.usable_tasks.keys())

        # Assign tasks to be completed. Tasks are assigned in no particular order, 
        # just however the dictionaries organize their keys.
        for i in range(len(player_cookies)):

            player_cookie = player_cookies[i]
            task_id = initial_task_ids[i]

            # Assign task to do
            self.initial_task_assignments[player_cookie] = self.task_generator.current_tasks[task_id]


            # Assign a list of tasks that each user can complete on their own

            index_of_first_task = i * TaskGenerator.NUM_TASKS_PER_PLAYER

            # initialize with empty list, so we can add tasks to it in loop
            self.user_tasks[player_cookie] = []
            for j in range(TaskGenerator.NUM_TASKS_PER_PLAYER):

                # figure out which task we can add from usable_tasks
                interactable_task_id = usable_task_ids[ (i * TaskGenerator.NUM_TASKS_PER_PLAYER) + j ]

                # add that task
                self.user_tasks[player_cookie].append(self.task_generator.usable_tasks[interactable_task_id])


    def task_failed(self):
        """Update the ship health and loss status when a task fails"""

        self.ship_health = self.ship_health - self.task_fail_damage
        self.has_lost = self.ship_health <= 0


    def bad_input(self):
        """
        Update the ship health and loss status when a user 
        presses a button that doesn't complete an active task
        """

        self.ship_health = self.ship_health - self.bad_input_damage
        self.has_lost = self.ship_health <= 0


    def task_completed(self):
        """
        Update the num_tasks_completed and win status
        when a user successfully completes a task
        """

        self.num_tasks_completed = self.num_tasks_completed + 1
        self.section_complete = self.num_tasks_completed >= self.num_tasks_to_complete


        










