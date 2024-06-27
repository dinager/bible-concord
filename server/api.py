import json
from http import HTTPStatus

from flask import Blueprint, Response, request

from server.logic.bible_book_parser import parse_book

concord_blueprint = Blueprint(
    "bible_concord_api",
    __name__,
)


@concord_blueprint.route("/hello", methods=["GET"])
def hello_world() -> str:
    return "Hello World!"


@concord_blueprint.route("/api/add_book", methods=["POST"])
def add_book() -> Response:
    """
    curl --location 'http://localhost:4200/api/add_book' --form 'textFile=@"/path/to/file.txt"' -F "bookName=genesis"
    """
    if "textFile" not in request.files:
        return Response(json.dumps({"error": "No file part"}), status=HTTPStatus.BAD_REQUEST)
    if "bookName" not in request.form:
        return Response(json.dumps({"error": "No book name"}), status=HTTPStatus.BAD_REQUEST)
    book_name = request.form.get("bookName")
    # Assuming the file is in the following format: tests/resources/genesis.txt
    file = request.files["textFile"]
    book_text = file.read().decode("utf-8")
    parsed_book = parse_book(book_name, book_text)
    return Response(
        response=f"received book with {parsed_book.num_chapters} chapters",
        status=HTTPStatus.OK,
        mimetype="text/html",
    )
