"""
Represents a specific task that players can complete

Written by Gabriel Brown
"""

class Task:

    def __init__(self, task_id, description, button_text):
        
        self.task_id = task_id
        self.description = description
        self.button_text = button_text