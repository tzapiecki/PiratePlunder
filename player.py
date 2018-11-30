"""
Keep track of information about each player in game
"""
import uuid

class Player:

    def __init__(self, user_id=""):
        """Constructor for player object. If no user_id is passed in, generate a new one"""

        if user_id == "":
            self.user_id = str(uuid.uuid4())
        else:
            self.user_id = user_id

        self.ready = False

    def __eq__(self, obj):

        return isinstance(obj, Player) and obj.user_id == self.user_id

    def __hash__(self):
        
        return id(self)