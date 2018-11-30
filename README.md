# PiratePlunder
A collaborative browser game for fun with your friends.

## How to set up your environment
1. Clone this repository
```
cd yourDirectory
git clone https://github.com/tzapiecki/PiratePlunder
cd PiratePlunder
```
2. Make sure you have the latest version of Python and pip installed, then set up your virtual environment
```
python3 -m venv venv
. ./venv/bin/activate
```
You should now see `(venv)` before each line of your command line prompt.  

3. With your virtual environment activated, install flask, socketio, and the eventlet extension
```
pip install flask
pip install flask-socketio --user
pip install eventlet --user
```
NOTE: You might not need to use the `--user` flag when installing SocketIO and Eventlet. I needed to in both cases, which is why I'm making it the default.

That's it! Remember to always activate your virtual environment with `. ./venv/bin/activate` in the `PiratePlunder` directory before you start the server.

## Playing the game
1. In the `PiratePlunder` directory, with the virtual environment activated, start up the server
```
python server.py
```
Go to the url listed in the terminal window, grab a friend, and start playing!  

Note 1: If you're just running the server locally (i.e. the url looks something like `http://127.0.0.1:5000`) you'll need to open up a page in two different browsers to get two players in the lobby and start the game, because players are tracked based on cookies.

Note 2: in the terminal window where you started the server, you can shut down the server at any time by entering `Ctrl + C`

## Project structure

### server.py
This is where the main Flask app lives. Our Flask app handles various url requests from the client-side and responds with a new page or information about the game.

### templates/...
The templates for the lobby and game page live in this folder.

### static/...
The login page and static images used in the game live in this folder.
