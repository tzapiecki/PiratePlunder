"""
Represents a specific task that players can complete

Written by Gabriel Brown
"""

class Task:

    def __init__(self, task_id, description, button_text, button_position):
        
        self.task_id = task_id
        self.description = description
        self.button_text = button_text
        self.button_position = button_position

    def __str__(self):

        print("\nTask_id: " + str(self.task_id))
        print("Description: " + self.description)
        print("Button label: " + self.button_text)
        print("Button position:" + str(self.button_position))

    def serialize(self):

        return {
            'task_id': self.task_id,
            'description': self.description,
            'button_text': self.button_text,
            'button_position': self.button_position
        }