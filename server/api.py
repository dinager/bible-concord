import json
from decimal import Decimal
from http import HTTPStatus

from flask import Blueprint, Response, request

from server.db_model.model.book import BookModel
from server.db_model.model.group import GroupModel
from server.db_model.model.phrase import PhraseModel
from server.db_model.model.word_appearance import WordAppearanceModel
from server.service.books_services import (
    add_book,
    get_book_content,
    get_book_names,
    get_books,
    get_num_chapters_in_book,
)
from server.service.chapters_services import get_num_verses_in_chapter
from server.service.group_services import add_group, add_word_to_group, get_groups, get_words_in_group
from server.service.phrase_services import add_phrase, get_phrase_references, get_phrases
from server.service.verses_services import get_num_words_in_verse
from server.service.words_services import get_word_text_context
from server.utils.timer import Timer

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
    success, res = get_book_names()
    if success is False:
        return Response(res, status=HTTPStatus.BAD_REQUEST)

    return Response(
        json.dumps(res),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )


@blueprint.route("/api/book/<book_name>/num_chapters/", methods=["GET"])
def get_num_chapters_in_book_api(book_name: str) -> Response:
    success, num_chapters = get_num_chapters_in_book(book_name)
    if success is False:
        return Response(num_chapters, status=HTTPStatus.BAD_REQUEST)

    return Response(
        str(num_chapters),
        status=HTTPStatus.OK,
        mimetype="text/html",
    )


@blueprint.route("/api/book/<book_name>/chapter/<int:chapter_num>/num_verses", methods=["GET"])
def get_num_verses_in_chapter_api(book_name: str, chapter_num: int) -> Response:
    success, verses_num = get_num_verses_in_chapter(book_name, chapter_num)
    if success is False:
        return Response(verses_num, status=HTTPStatus.BAD_REQUEST)

    return Response(
        str(verses_num),
        status=HTTPStatus.OK,
        mimetype="text/html",
    )


@blueprint.route(
    "/api/book/<book_name>/chapter/<int:chapter_num>/verse/<int:verse_num>/num_words", methods=["GET"]
)
def get_num_words_in_verse_api(book_name: str, chapter_num: int, verse_num: int) -> Response:
    success, num_words = get_num_words_in_verse(book_name, chapter_num, verse_num)
    if success is False:
        return Response(num_words, status=HTTPStatus.BAD_REQUEST)
    return Response(
        str(num_words),
        status=HTTPStatus.OK,
        mimetype="text/html",
    )


@blueprint.route("/api/words/", methods=["POST"])
def filter_words_api() -> Response:
    user_filters = request.json["filters"]
    page_index = request.json["pageIndex"]
    page_size = request.json["pageSize"]
    keys = ["wordStartsWith", "book", "chapter", "verse", "wordPosition", "groupName"]
    filters = {key: user_filters[key] for key in keys if user_filters.get(key)}

    filtered_words, total = WordAppearanceModel.get_filtered_words_paginate(filters, page_index, page_size)
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
    keys = ["book", "chapter", "verse", "wordPosition"]
    filters = {key: user_filters[key] for key in keys if user_filters.get(key)}

    with Timer("get_word_appearances_paginate", log_params={"word": word, "filters": filters}):
        word_appearances, total = WordAppearanceModel.get_word_appearances_paginate(
            word.lower(), filters, page_index, page_size
        )
    return Response(
        json.dumps({"wordAppearances": word_appearances, "total": total}),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )


@blueprint.route(
    "/api/text_context/book/<book>/chapter/<int:chapter>/verse/<int:verse>",
    methods=["GET"],
)
def get_word_text_context_api(book: str, chapter: int, verse: int) -> Response:
    with Timer("get_word_text_context", log_params={"book": book, "chapter": chapter, "verse": verse}):
        success, text = get_word_text_context(book, chapter, verse)
    if success is False:
        return Response(text, status=HTTPStatus.BAD_REQUEST)
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
    success, res = add_group(group_name)
    if success is False:
        return Response(res, status=HTTPStatus.BAD_REQUEST)

    return Response(
        res,
        status=HTTPStatus.OK,
        mimetype="text/html",
    )


@blueprint.route("/api/groups", methods=["GET"])
def get_groups_api() -> Response:
    success, res = get_groups()
    if success is False:
        return Response(res, status=HTTPStatus.BAD_REQUEST)

    return Response(
        res,
        status=HTTPStatus.OK,
        mimetype="application/json",
    )


@blueprint.route("/api/group/<group_name>/words", methods=["GET"])
def get_words_in_group_api(group_name: str) -> Response:
    group_name = group_name.lower()
    success, res = get_words_in_group(group_name)
    if success is False:
        return Response(res, status=HTTPStatus.BAD_REQUEST)

    return Response(
        json.dumps({"words": res}),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )


@blueprint.route("/api/groups/add_word", methods=["POST"])
def add_word_to_group_api() -> Response:
    if "groupName" not in request.json or "word" not in request.json:
        return Response("Request should contain 'groupName' and 'word", status=HTTPStatus.BAD_REQUEST)
    group_name = request.json["groupName"].lower()
    word = request.json["word"].lower()
    success, res = add_word_to_group(group_name, word)
    if success is False:
        return Response(res, status=HTTPStatus.BAD_REQUEST)

    return Response(
        res,
        status=HTTPStatus.OK,
        mimetype="text/html",
    )


@blueprint.route("/api/group/<group_name>/word_appearances_index", methods=["GET"])
def get_group_word_appearances_index_api(group_name: str) -> Response:
    group_name = group_name.lower()
    with Timer("get_group_word_appearances_index", log_params={"group_name": group_name}):
        res = WordAppearanceModel.get_group_word_appearances_index(group_name)

    return Response(
        json.dumps(res),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )


@blueprint.route("/api/phrases", methods=["GET"])
def get_phrases_api() -> Response:
    success, res = get_phrases()
    if success is False:
        return Response(res, status=HTTPStatus.BAD_REQUEST)

    return Response(
        res,
        status=HTTPStatus.OK,
        mimetype="application/json",
    )


@blueprint.route("/api/add_phrase", methods=["POST"])
def add_phrase_api() -> Response:
    if "phraseText" not in request.json:
        return Response("Request should contain 'phraseText'", status=HTTPStatus.BAD_REQUEST)
    # todo: rename phraseText -> phraseText
    phrase_text = request.json["phraseText"].lower()
    with Timer("add_phrase", log_params={"phrase_text": phrase_text}):
        success, res = add_phrase(phrase_text)
    if success is False:
        return Response(res, status=HTTPStatus.BAD_REQUEST)

    return Response(
        res,
        status=HTTPStatus.OK,
        mimetype="text/html",
    )


@blueprint.route("/api/phrase/<phrase_text>/reference", methods=["GET"])
def get_phrase_reference_api(phrase_text: str) -> Response:
    phrase_text = phrase_text.lower()
    with Timer("get_phrase_references", log_params={"phrase_text": phrase_text}):
        res = get_phrase_references(phrase_text)

    return Response(
        json.dumps(res),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )


@blueprint.route("/api/book-to-delete/<book_name>", methods=["DELETE"])
def delete_book_api(book_name: str) -> Response:
    with Timer("delete_book_by_title", log_params={"book_name": book_name}):
        BookModel.delete_book_by_title(book_name)
    return Response(
        "ok",
        status=HTTPStatus.OK,
        mimetype="text/html",
    )


@blueprint.route("/api/group-to-delete/<group_name>", methods=["DELETE"])
def delete_group_api(group_name: str) -> Response:
    GroupModel.delete_group_by_name(group_name)
    return Response(
        "ok",
        status=HTTPStatus.OK,
        mimetype="text/html",
    )


@blueprint.route("/api/phrase-to-delete/<phrase_text>", methods=["DELETE"])
def delete_phrase_api(phrase_text: str) -> Response:
    PhraseModel.delete_phrase(phrase_text)
    return Response(
        "ok",
        status=HTTPStatus.OK,
        mimetype="text/html",
    )


@blueprint.route("/api/general_stats", methods=["GET"])
def get_general_stats_api() -> Response:
    book_length = len(BookModel.get_all_books())
    group_length = len(GroupModel.get_all_groups_names())
    phrase_length = len(PhraseModel.get_all_phrases())

    statistics = {
        "Total Number of Books": book_length,
        "Total Number of Groups": group_length,
        "Total Number of Phrases": phrase_length,
    }

    return Response(
        json.dumps(statistics),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )


@blueprint.route("/api/books/<book_name>/stats", methods=["GET"])
@blueprint.route("/api/books/stats", methods=["GET"])
def get_book_stats_api(book_name: str | None = "") -> Response:
    if book_name == "":
        book_name = None
    res = BookModel.get_book_statistics(book_name)

    def decimal_to_float(o: object) -> float:
        if isinstance(o, Decimal):
            return float(o)
        raise TypeError

    # Convert Decimal values in the response
    res_serializable = json.dumps(res, default=decimal_to_float)

    return Response(
        res_serializable,
        status=HTTPStatus.OK,
        mimetype="application/json",
    )
