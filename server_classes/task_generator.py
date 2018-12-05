"""
Used to generate new tasks that haven't been done before and are also
possible given current conditions

By Gabriel Brown, 11/30/2018
"""
from .task import Task
import random

class TaskGenerator:


    # BIG TODO: swap lists of tasks to dictionaries that have task_ids as keys


    NUM_TASKS_PER_PLAYER = 3

    tasks = []  # TODO: fill this up with all possible tasks

    # fill with sample task data
    for i in range(20):

        task_id = i
        description = "Complete Task #" + str(i) + "!"
        button_text = "Push this button to complete Task #" + str(i)
        button_position = (50, 50)

        tasks.append(Task(task_id, description, button_text, button_position))


    def __init__(self, num_players):

        self.num_players = num_players
        self.usable_tasks = {}      # KEY: task_id, VALUE = task
        self.current_tasks = {}     # KEY: task_id, VALUE = task

        self.update_usable_tasks()
        self.generate_initial_tasks()

        print("Total tasks:")
        print(self.tasks)
        print("\nUsable tasks:")
        print(self.usable_tasks)
        print("\nCurrent tasks:")
        print(self.current_tasks)


    def new_task(self, old_task_id):
        """
        Randomnly pick the next task from usable_tasks, provided it's not currently active
        """

        new_task = self.current_tasks[old_task_id]

        while new_task.task_id in self.current_tasks:

            next_index = random.randrange(0, len(self.usable_tasks))
            new_task = usable_tasks[next_index]

        # Remove the old task and keep track of new one
        current_tasks.remove(old_task_id)
        current_tasks[new_task.task_id] = new_task

        return new_task


    def update_usable_tasks(self):
        """Swap out usuable_tasks with a new list of tasks"""

        # Make sure we have enough tasks. Multiplied by 2 because we have to have a completely new set
        if len(self.tasks) < (TaskGenerator.NUM_TASKS_PER_PLAYER * self.num_players) * 2:
            print("Make more tasks!")
            return

        # Otherwise go on
        new_usable_tasks = {}

        # Swap out usable_tasks with a new random set of tasks
        while len(new_usable_tasks) < TaskGenerator.NUM_TASKS_PER_PLAYER * self.num_players:

            next_index = random.randrange(0, len(self.tasks))
            next_task = self.tasks[next_index]

            if (next_task.task_id not in self.usable_tasks) and (next_task.task_id not in new_usable_tasks):

                new_usable_tasks[next_task.task_id] = next_task


        self.usable_tasks = new_usable_tasks


    def generate_initial_tasks(self):
        """Populate current_tasks with the initial set of tasks, one for each player"""

        # Make sure we have enough tasks to begin with
        if len(self.tasks) < self.num_players or len(self.usable_tasks) < self.num_players:
            print("Make more tasks!")
            return


        # Otherwise continue
        usable_task_keys = list(self.usable_tasks.keys())

        # Keep going until we have a task for each player
        while len(self.current_tasks) < self.num_players:

            next_index = random.randrange(0, len(usable_task_keys))
            next_task_key = usable_task_keys[next_index]

            # Keep picking random keys until we find one that's not already used
            while next_task_key in self.current_tasks:

                next_index = random.randrange(0, len(usable_task_keys))
                next_task_key = usable_task_keys[next_index]

            # Add new task to the current list 
            self.current_tasks[next_task_key] = self.usable_tasks[next_task_key]








