import json
from http import HTTPStatus

from flask import Blueprint, Response, request

from server.logic.api_mocks import MOCK_BOOKS, MOCK_BOOKS_NAMES, get_book_content_mock
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
    # todo: use json schema validator
    if "textFile" not in request.files:
        return Response("No file part", status=HTTPStatus.BAD_REQUEST)
    if "bookName" not in request.form:
        return Response("No book name", status=HTTPStatus.BAD_REQUEST)
    # if "division" not in request.form:
    #     return Response("No division", status=HTTPStatus.BAD_REQUEST)
    book_name = request.form.get("bookName")
    # Assuming the file is in the following format: tests/resources/genesis.txt
    file = request.files["textFile"]
    book_text = file.read().decode("utf-8")
    parsed_book = parse_book(book_name, book_text)
    return Response(
        f"received book with {parsed_book.num_chapters} chapters",
        status=HTTPStatus.OK,
        mimetype="text/html",
    )


@concord_blueprint.route("/api/get_books", methods=["GET"])
def get_books() -> Response:
    """
    curl 'http://localhost:4200/api/get_books'
    """
    return Response(
        json.dumps({"books": MOCK_BOOKS}),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )


@concord_blueprint.route("/api/get_book_content/<book_name>", methods=["GET"])
def get_book_content(book_name: str) -> Response:
    """
    curl 'http://localhost:4200/api/get_book_content/Genesis'
    """
    if book_name.lower() not in MOCK_BOOKS_NAMES:
        return Response(
            f"book {book_name} not found",
            status=HTTPStatus.NOT_FOUND,
            mimetype="text/html",
        )
    book_content = get_book_content_mock(book_name)
    return Response(
        book_content,
        status=HTTPStatus.OK,
        mimetype="text/html",
    )
