from flask import Flask

flask_app = Flask(__name__)
flask_app.config.from_object("server.config.Config")
