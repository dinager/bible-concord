import json
import traceback
from typing import Any, Dict, List, Tuple

from server.db_model.model.book import BookModel
from server.db_model.model.phrase import PhraseModel
from server.db_model.model.phrase_reference import PhraseReferenceModel


def add_phrase(phrase_name: str) -> Tuple[bool, str]:
    try:
        phrase_name = phrase_name.lower()
        if PhraseModel.does_phrase_exist(phrase_name):
            return False, f"phrase {phrase_name} already exists"

        PhraseModel.insert_phrase_to_phrase_table(phrase_name)
        phrase_id = PhraseModel.get_phrase_id(phrase_name)
        if not phrase_id:
            return False, f"phrase id for phrase {phrase_name} wasn't found"

        res = PhraseReferenceModel.add_references_of_phrases(phrase_name, phrase_id)
        if res == -1:
            PhraseModel.delete_phrase_from_phrase_table(phrase_name)
            return False, f"phrase name {phrase_name} wasn't found in the text"
        if res == 0:
            return True, f"phrase {phrase_name} added successfully"

    except Exception as e:
        print(traceback.format_exc())
        return False, str(e)

    return False, "Unexpected error occurred"


def get_phrases() -> Tuple[bool, str]:
    # the return string is a JSON string
    try:
        phrase_names = PhraseModel.get_all_phrases_names()
        return True, json.dumps({"phrases": list(phrase_names)})

    except Exception as e:
        print(traceback.format_exc())
        return False, str(e)


def get_phrase_references(phrase_name: str) -> Dict[str, List[Dict[str, Any]]]:
    phrase_id = PhraseModel.get_phrase_id(phrase_name)
    references = PhraseReferenceModel.get_all_phrase_references(phrase_id)
    phrase_references: Dict[str, List[Dict[str, Any]]] = {}

    for reference in references:
        book_title = BookModel.get_book_title_by_id(reference.get("book_id"))

        phrase_reference = {
            "title": book_title,
            "chapter_num": reference.get("chapter_num"),
            "verse_num": reference.get("verse_num"),
            "word_position": reference.get("word_position"),
        }

        # If phrase_name is not in dictionary, initialize with empty list
        if phrase_name not in phrase_references:
            phrase_references[phrase_name] = []

        # Append the reference to the corresponding phrase
        phrase_references[phrase_name].append(phrase_reference)

    return phrase_references


def get_phrase_context(
    phrase_name: str, book_title: str, chapter_num: int, verse_num: int, word_position: int
) -> Tuple[bool, str]:
    try:
        book_id = BookModel.get_book_id(book_title)
        fetched_context = PhraseReferenceModel.construct_context_from_db(book_id, chapter_num, verse_num)
        return True, fetched_context

    except Exception as e:
        print(traceback.format_exc())
        return False, str(e)
