from flask_cors import CORS

from server.api import blueprint
from server.app_instance import flask_app
from server.db_instance import db

db.init_app(flask_app)
flask_app.app_context().push()
flask_app.register_blueprint(blueprint)

CORS(flask_app)

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=4200, debug=flask_app.debug)
