import json
from http import HTTPStatus

from flask import Blueprint, Response, request

concord_blueprint = Blueprint(
    "bible_concord_api",
    __name__,
)


@concord_blueprint.route("/hello", methods=["GET"])
def hello_world() -> str:
    return "Hello World!"


@concord_blueprint.route("/api/add_book", methods=["POST"])
def add_book() -> Response:
    if "file" not in request.files:
        return Response(json.dumps({"error": "No file part"}), status=HTTPStatus.BAD_REQUEST)

    # Assuming the file contains comma-separated values
    file = request.files["file"]
    book_data = file.read().decode("utf-8")
    lines = book_data.splitlines()
    return Response(response=f"lines: {len(lines)}", status=HTTPStatus.OK, mimetype="text/html")
