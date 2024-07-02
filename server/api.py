import json
from http import HTTPStatus

from flask import Blueprint, Response, request

from server.logic.bible_book_parser import parse_text_to_book_chapters
from server.logic.mocks.api_mocks import (
    MOCK_BOOKS,
    MOCK_BOOKS_NAMES,
    get_all_words_paginate_mock,
    get_book_content_mock,
    get_filtered_words_paginate_mock,
    get_num_chapters_in_book_mock,
    get_num_verses_in_chapter_mock,
    get_word_appearances_paginate_mock, get_num_words_in_verse_mock,
)
from server.logic.structures import BibleBook

blueprint = Blueprint(
    "bible_concord_api",
    __name__,
)


@blueprint.route("/hello", methods=["GET"])
def hello_world() -> str:
    return "Hello World!"


@blueprint.route("/api/add_book", methods=["POST"])
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
    book_chapters = parse_text_to_book_chapters(book_text)
    bible_book = BibleBook(
        name=book_name,
        num_chapters=len(book_chapters),
        chapters=book_chapters,
    )
    return Response(
        f"received book with {bible_book.num_chapters} chapters",
        status=HTTPStatus.OK,
        mimetype="text/html",
    )


@blueprint.route("/api/books", methods=["GET"])
def get_books() -> Response:
    """
    curl 'http://localhost:4200/api/books'
    """
    return Response(
        json.dumps({"books": MOCK_BOOKS}),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )


@blueprint.route("/api/book_content/<book_name>", methods=["GET"])
def get_book_content(book_name: str) -> Response:
    """
    curl 'http://localhost:4200/api/book_content/Genesis'
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


@blueprint.route("/api/book_names", methods=["GET"])
def get_book_names() -> Response:
    """
    curl 'http://localhost:4200/api/books'
    """
    book_names = [book["name"] for book in MOCK_BOOKS]
    return Response(
        json.dumps(book_names),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )


@blueprint.route("/api/book/<book_name>/num_chapters/", methods=["GET"])
def get_num_chapters_in_book(book_name: str) -> Response:
    if book_name.lower() not in MOCK_BOOKS_NAMES:
        return Response(
            f"book {book_name} not found",
            status=HTTPStatus.NOT_FOUND,
            mimetype="text/html",
        )
    num_chapters: int = get_num_chapters_in_book_mock(book_name)
    return Response(
        str(num_chapters),
        status=HTTPStatus.OK,
        mimetype="text/html",
    )


@blueprint.route("/api/book/<book_name>/chapter/<int:chapter_num>/num_verses", methods=["GET"])
def get_num_verses_in_chapter(book_name: str, chapter_num: int) -> Response:
    num_chapters: int = get_num_verses_in_chapter_mock(book_name, chapter_num)
    return Response(
        str(num_chapters),
        status=HTTPStatus.OK,
        mimetype="text/html",
    )


@blueprint.route(
    "/api/book/<book_name>/chapter/<int:chapter_num>/verse/<int:verse_num>/num_words", methods=["GET"]
)
def get_num_words_in_verse(book_name: str, chapter_num: int, verse_num: int) -> Response:
    num_chapters: int = get_num_words_in_verse_mock(book_name, chapter_num, verse_num)
    return Response(
        str(num_chapters),
        status=HTTPStatus.OK,
        mimetype="text/html",
    )


@blueprint.route("/api/words/", methods=["POST"])
def filter_words() -> Response:
    user_filters = request.json["filters"]
    page_index = request.json["pageIndex"]
    page_size = request.json["pageSize"]
    if not user_filters or all(not value for value in user_filters.values()):
        filtered_words, total = get_all_words_paginate_mock(page_index, page_size)
    else:
        filters = {}
        # todo: send user_filters directly..
        if user_filters.get("wordStartsWith"):
            filters["wordStartsWith"] = user_filters["wordStartsWith"].lower()
        if user_filters.get("book"):
            filters["book"] = user_filters["book"].lower()
            if user_filters.get("chapter"):
                filters["chapter"] = user_filters["chapter"]
                if user_filters.get("verse"):
                    filters["verse"] = user_filters["verse"]

        filtered_words, total = get_filtered_words_paginate_mock(filters, page_index, page_size)
    return Response(
        json.dumps({"words": filtered_words, "total": total}),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )


@blueprint.route("/api/word/<word>", methods=["POST"])
def get_word_appearances(word: str) -> Response:
    user_filters = request.json["filters"]
    page_index = request.json["pageIndex"]
    page_size = request.json["pageSize"]
    word_appearances, total = get_word_appearances_paginate_mock(
        word.lower(), user_filters, page_index, page_size
    )
    return Response(
        json.dumps({"wordAppearances": word_appearances, "total": total}),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )
