from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World"

@app.route("/")
def create():
    return "create"

@app.route("/")
def update():
    return "update"

@app.route("/")
def remove():
    return "remove"

@app.route("/")
def get():
    return "get"

if __name__ == "__main__":
    app.run()