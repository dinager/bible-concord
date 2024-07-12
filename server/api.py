import json
from http import HTTPStatus

from flask import Blueprint, Response, request

from server.logic.books_services import add_book, get_book_content, get_books
from server.logic.mocks.api_mocks import (
    MOCK_BOOKS,
    MOCK_BOOKS_NAMES,
    MOCK_WORDS_IN_GROUPS,
    get_all_words_paginate_mock,
    get_filtered_words_paginate_mock,
    get_num_chapters_in_book_mock,
    get_num_verses_in_chapter_mock,
    get_num_words_in_verse_mock,
    get_word_appearances_paginate_mock,
    get_word_text_context_mock,
)

blueprint = Blueprint(
    "bible_concord_api",
    __name__,
)


@blueprint.route("/ping", methods=["GET"])
def ping() -> str:
    return "pong"


@blueprint.route("/api/add_book", methods=["POST"])
def add_book_api() -> Response:
    """
    curl --location 'http://localhost:4200/api/add_book' --form 'textFile=@"/path/to/file.txt"' -F "bookName=genesis" -F "division=Torah"
    """
    # todo: use json schema validator
    if "textFile" not in request.files:
        return Response("No file part", status=HTTPStatus.BAD_REQUEST)
    if "bookName" not in request.form or "division" not in request.form:
        return Response(
            "Request form should contain 'bookName' and 'division'", status=HTTPStatus.BAD_REQUEST
        )

    # Assuming the file is in the following format: tests/resources/genesis.txt
    success, res = add_book(request.form["bookName"], request.files["textFile"], request.form["division"])
    if success is False:
        return Response(res, status=HTTPStatus.BAD_REQUEST)

    return Response(
        res,
        status=HTTPStatus.OK,
        mimetype="text/html",
    )


@blueprint.route("/api/books", methods=["GET"])
def get_books_api() -> Response:
    """
    curl 'http://localhost:4200/api/books'
    """

    success, res = get_books()
    if success is False:
        return Response(res, status=HTTPStatus.BAD_REQUEST)

    return Response(
        res,
        status=HTTPStatus.OK,
        mimetype="application/json",
    )


@blueprint.route("/api/book_content/<book_name>", methods=["GET"])
def get_book_content_api(book_name: str) -> Response:
    """
    curl 'http://localhost:4200/api/book_content/Genesis'
    """
    success, res = get_book_content(book_name)
    if success is False:
        return Response(res, status=HTTPStatus.BAD_REQUEST)

    return Response(
        res,
        status=HTTPStatus.OK,
        mimetype="text/html",
    )


@blueprint.route("/api/book_names", methods=["GET"])
def get_book_names_api() -> Response:
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
def get_num_chapters_in_book_api(book_name: str) -> Response:
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
def get_num_verses_in_chapter_api(book_name: str, chapter_num: int) -> Response:
    num_chapters: int = get_num_verses_in_chapter_mock(book_name, chapter_num)
    return Response(
        str(num_chapters),
        status=HTTPStatus.OK,
        mimetype="text/html",
    )


@blueprint.route(
    "/api/book/<book_name>/chapter/<int:chapter_num>/verse/<int:verse_num>/num_words", methods=["GET"]
)
def get_num_words_in_verse_api(book_name: str, chapter_num: int, verse_num: int) -> Response:
    num_chapters: int = get_num_words_in_verse_mock(book_name, chapter_num, verse_num)
    return Response(
        str(num_chapters),
        status=HTTPStatus.OK,
        mimetype="text/html",
    )


@blueprint.route("/api/words/", methods=["POST"])
def filter_words_api() -> Response:
    user_filters = request.json["filters"]
    page_index = request.json["pageIndex"]
    page_size = request.json["pageSize"]
    if not user_filters or all(not value for value in user_filters.values()):
        filtered_words, total = get_all_words_paginate_mock(page_index, page_size)
    else:
        keys = ["wordStartsWith", "book", "chapter", "verse", "indexInVerse"]
        filters = {key: user_filters[key] for key in keys if user_filters.get(key)}

        filtered_words, total = get_filtered_words_paginate_mock(filters, page_index, page_size)
    return Response(
        json.dumps({"words": filtered_words, "total": total}),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )


@blueprint.route("/api/word/<word>", methods=["POST"])
def get_word_appearances_api(word: str) -> Response:
    user_filters = request.json["filters"]
    page_index = request.json["pageIndex"]
    page_size = request.json["pageSize"]
    keys = ["book", "chapter", "verse", "indexInVerse"]
    filters = {key: user_filters[key] for key in keys if user_filters.get(key)}

    word_appearances, total = get_word_appearances_paginate_mock(word.lower(), filters, page_index, page_size)
    return Response(
        json.dumps({"wordAppearances": word_appearances, "total": total}),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )


@blueprint.route(
    "/api/text_context/<word>/book/<book>/chapter/<int:chapter>/verse/<int:verse>/index/<int:index>",
    methods=["GET"],
)
def get_word_text_context_api(word: str, book: str, chapter: int, verse: int, index: int) -> Response:
    text = get_word_text_context_mock(word.lower(), book, chapter, verse, index)
    return Response(
        text,
        status=HTTPStatus.OK,
        mimetype="text/html",
    )


@blueprint.route("/api/add_group", methods=["POST"])
def add_group_api() -> Response:
    if "groupName" not in request.json:
        return Response("Request should contain 'groupName'", status=HTTPStatus.BAD_REQUEST)
    group_name = request.json["groupName"].lower()
    if group_name in MOCK_WORDS_IN_GROUPS:
        return Response(
            f"group {group_name} already exists",
            status=HTTPStatus.BAD_REQUEST,
            mimetype="text/html",
        )
    MOCK_WORDS_IN_GROUPS[group_name] = []

    return Response(
        f"group {group_name} added successfully",
        status=HTTPStatus.OK,
        mimetype="text/html",
    )


@blueprint.route("/api/groups", methods=["GET"])
def get_groups_api() -> Response:
    group_names = MOCK_WORDS_IN_GROUPS.keys()
    return Response(
        json.dumps({"groups": list(group_names)}),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )


@blueprint.route("/api/group/<group_name>/words", methods=["GET"])
def get_words_in_group_api(group_name: str) -> Response:
    group_name = group_name.lower()
    if group_name not in MOCK_WORDS_IN_GROUPS:
        return Response(
            f"group {group_name} not found",
            status=HTTPStatus.NOT_FOUND,
            mimetype="text/html",
        )
    words_in_group: list[str] = MOCK_WORDS_IN_GROUPS[group_name]
    return Response(
        json.dumps({"words": words_in_group}),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )


@blueprint.route("/api/groups/add_word", methods=["POST"])
def add_word_to_group_api() -> Response:
    if "groupName" not in request.json or "word" not in request.json:
        return Response("Request should contain 'groupName' and 'word", status=HTTPStatus.BAD_REQUEST)
    group_name = request.json["groupName"].lower()
    word = request.json["word"].lower()
    if group_name not in MOCK_WORDS_IN_GROUPS:
        return Response(
            f"group {group_name} not found",
            status=HTTPStatus.NOT_FOUND,
            mimetype="text/html",
        )
    if word in MOCK_WORDS_IN_GROUPS[group_name]:
        return Response(
            f"word {word} already exists in group {group_name}",
            status=HTTPStatus.BAD_REQUEST,
            mimetype="text/html",
        )
    MOCK_WORDS_IN_GROUPS[group_name].append(word)
    return Response(
        f"word {word} added to group {group_name} successfully",
        status=HTTPStatus.OK,
        mimetype="text/html",
    )
