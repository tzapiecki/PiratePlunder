"""
Used to generate new tasks that haven't been done before and are also
possible given current conditions

By Gabriel Brown, 11/30/2018
"""
from task import Task

class TaskGenerator:

    tasks = []  # TODO: fill this up with all possible tasks


    def __init__(self):

        self.usable_tasks = tasks
        self.current_tasks = []


    def new_task(self):

        # TODO: randomnly pick a task from usable_tasks to be assigned next

        pass


    def task_complete(self, task_id):

        # TODO: remove this task from usable_tasks

        pass