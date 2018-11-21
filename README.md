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

3. With your virtual environment activated, install flask and socketio
```
pip install flask
pip install flask-socketio
```
NOTE: When you install socketio, you may need to include the `--user` flag. For those unfamiliar with flags, you just need to enter 
```
pip install flask-socketio --user
``` 
instead of 
```
pip install flask-socketio
```

That's it! Remember to always activate your virtual environment with `. ./venv/bin/activate` in the `PiratePlunder` directory before you start the server.

## Playing the game
1. In the `PiratePlunder` directory, with the virtual environment activated, start up the server
```
python3 server.py
```
Go to the url it lists, grab a friend, and start playing!  

Note: in the terminal window where you started the server, you can shut down the server at any time by entering `Ctrl + C`

## Project structure
TODO
