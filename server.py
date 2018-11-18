from flask import Flask, render_template
app = Flask(__name__, static_url_path='')


"""
Routes to new pages
"""
@app.route('/')
def index():
    return app.send_static_file('login.html')

@app.route('/lobby/<lobby_id>')
def lobby(lobby_id):
    return render_template("lobby.html", lobby_id=lobby_id)

@app.route('/game/<lobby_id>')
def game(lobby_id):
    return render_template("game.html", lobby_id=lobby_id)


"""
Routes to pass around information
"""


if __name__ == '__main__':
    app.run(debug=True)