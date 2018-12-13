"""
Game Lobby class to keep information about each player in a game

Written by Trevor Zapiecki and Gabriel Brown
"""

from .player import Player
from . import events
from .task_generator import TaskGenerator

class GameLobby:

    INITIAL_NUM_TASKS_TO_COMPLETE = 5       
    INITIAL_TASK_COMPLETION_TIME = 15000    # In milliseconds

    def __init__(self, lobby_id, numPlayers):
        """Constructor for Lobby"""

        self.lobby_id = lobby_id
        self.numPlayers = numPlayers
        self.connectedPlayers = 0
        self.players = {}                   # KEY: user_id/cookies, VALUE: Player object

        # KEY: user/id cookie, VALUE: first task that user has to complete
        self.initial_task_assignments = {}

        # KEY: userid/cookie, VALUE: a list of tasks that this particular 
        # user can complete (should appear with buttons on their screen)
        self.user_tasks = {}


        self.ship_health = 100              # The overall ship health

        self.task_fail_damage = 10          # The amount of damage failing a task deals to the ship
        self.bad_input_damage = 5           # The amount of damage pressing a the wrong button deals to the ship

        # The number of tasks players must complete before moving on to a new sector
        self.num_tasks_to_complete = self.INITIAL_NUM_TASKS_TO_COMPLETE

        # The number of tasks players have actually completed
        self.num_tasks_completed = 0        

        self.has_won = False
        self.section_complete = False

        self.section_number = 0
        self.task_completion_time = self.INITIAL_TASK_COMPLETION_TIME  # The time alotted to complete each assigned task in milliseconds. 


    def add_player(self, player):
        self.players[player.user_id] = player

    
    def start_game(self):
        """This should be called whenever all the players connect to a game for the first time"""

        self.task_generator = TaskGenerator(len(self.players))
        self.adjust_challenge()
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

        if self.has_lost:
            self.section_number = 0


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

        if self.section_complete:
            self.section_number += 1


    def adjust_challenge(self):
        """
        Update the task completion time and and the number of 
        tasks to complete based on the section number 
        and number of players
        """

        # Base time should be 10 seconds plus 2 seconds per player, then subtract
        # 1 second each time we go up a section
        self.task_completion_time = self.INITIAL_TASK_COMPLETION_TIME + (self.numPlayers - 2)*2000 - self.section_number*1000 

        # Add an additional task per player when the section increases
        self.num_tasks_to_complete = self.INITIAL_NUM_TASKS_TO_COMPLETE + (self.section_number * self.numPlayers)       


    def reset(self):
        """
        Reset win conditions and ship health, ask the task generator
        for a new set of usable tasks, and assign them to the players
        """

        self.ship_health = 100
        self.has_won = False
        self.has_lost = False
        self.task_generator.new_section()
        self.adjust_challenge()
        self.assign_tasks()


        










