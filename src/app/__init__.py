from flask import Flask

def create_app():
    app = Flask(__name__)
    @app.route("/")
    def hello():
        return b"Hello World!"
    return app