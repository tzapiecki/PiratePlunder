from flask import Flask, Response, render_template, redirect
app = Flask(__name__)

@app.route('/')
def index():
    return redirect('static/index.html')

if __name__ == '__main__':
    app.run(debug=True)