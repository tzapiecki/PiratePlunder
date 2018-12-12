"""
Used to generate new tasks that haven't been done before and are also
possible given current conditions
Written by Gabriel Brown
"""
from .task import Task
import random

class TaskGenerator:

    NUM_TASKS_PER_PLAYER = 4

    # The master list of tasks. A selection of these are assigned to usable tasks,
    # based on the number of players and how many tasks should be assigned to each player
    tasks = []

    # Initialize all our custom tasks
    # Note: would be better to either randomnly generate these or
    # store them in a text file or database or something
    tasks.append(Task(0, "Rocks incoming! HARD TO PORT!", "Turn Portside", (100, 95)))
    tasks.append(Task(1, "To the east, an enemy vessel! Take us Starboard!", "Turn Starboard", (600, 95)))
    tasks.append(Task(2, "There's a rough wind coming, trim the jib before it hits us.", "Pull down Jib", (620, 110)))
    tasks.append(Task(3, "We're going the wrong direction. Spin the tiller! ", "Turn Tiller", (130, 70)))
    tasks.append(Task(4, "The enemy's about to fire! Take cover and save yourself!", "Take cover", (50, 100)))
    tasks.append(Task(5, "Load the cannons and prepare to fire!", "Load cannons", (70, 100)))
    tasks.append(Task(6, "Arr, there goes my monkey. Grab him for me, will you?", "Catch Monkey", (100, 100)))
    tasks.append(Task(7, "The cannons be ready! FIRE AWAY!", "Fire the cannons", (50, 10)))
    tasks.append(Task(8, "Your parrot looks a bit lonely, Give him some love, will ya?", "Pet the Parrot", (50, 10)))
    tasks.append(Task(9, "What arrrrrr ya lookin at, huh? You better keep your peepers away from me eyepatch, or I'll gut ya.", "Look away from eyepatch", (50, 10)))
    tasks.append(Task(10, "We've got a traitor on board. Ready the plank.", "Lower the plank", (50, 10)))
    tasks.append(Task(11, "Is that a real gold doubloon? Bite it and tell me!", "Bite the doubloon", (50, 10)))
    tasks.append(Task(12, "Arrrr, what lies ahead? Break out your telescope and tell me what's on the horizon.", "Scan the horizon", (50, 10)))
    tasks.append(Task(13, "Storm ahead. Best give Davey Jones his dues, else he'll be taking more souls tonight", "Drop Dave Jones offering into the sea", (50, 10)))
    tasks.append(Task(14, "We're out of cannonballs! Fill the cannons with whatever you can find!", "Load cannons with silverware", (50, 10)))
    tasks.append(Task(15, "A brawl be breakin out on the main deck. Unload your pistol and silence that rabble.", "Stop brawl", (50, 10)))
    tasks.append(Task(16, "That lad has quite a bounty! SEIZE HIM!", "Capture bounty", (50, 10)))


    # # fill with sample task data
    # for i in range(7, 12):

    #     task_id = i
    #     description = "Complete Task #" + str(i) + "!"
    #     button_text = "Push this button to complete Task #" + str(i)
    #     button_position = (50 + 10*i, 50 + 10*i)

    #     tasks.append(Task(task_id, description, button_text, button_position))


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

        new_task = self.current_tasks.get(old_task_id, None)
        if new_task is None:
            return None

        usable_task_keys = list(self.usable_tasks.keys())

        while new_task.task_id in self.current_tasks:

            next_index = random.randrange(0, len(self.usable_tasks))
            new_task = self.usable_tasks[usable_task_keys[next_index]]

        # Remove the old task and keep track of new one
        self.current_tasks.pop(old_task_id)
        self.current_tasks[new_task.task_id] = new_task

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



    def new_section(self):
        """Update usable_tasks and set up initial tasks"""

        self.update_usable_tasks()
        self.current_tasks.clear()
        self.generate_initial_tasks()
