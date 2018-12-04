"""
A bunch of constants holding the string names of different socketio events.

Written by Gabriel Brown
"""

""" Lobby events """

# emitted by server when there are at least two clients in lobby 
# and everyone has readied up
GAME_LOAD = "game_load"

GAME_START = "game_start"

PLAYER_JOINED = "player_joined"

PLAYER_DISCONNECTED = "player_disconnected"

LOBBY_STATUS_CHANGED = "lobby_status_changed"


""" In-game events """

# emitted by server when client input results in a completed task
TASK_COMPLETE = "task_complete"

# emitted by server when a client tells it that a task has been failed
TASK_FAILED = "task_failed"

# emitted by server when any client sends input that doesn't complete a task
BAD_INPUT = "bad_input"

# emitted by server when enough tasks have been completed to move
# to new section
SECTION_COMPLETE = "section_complete"

# emitted by server when ship health is too low
GAME_OVER = "game_over"

