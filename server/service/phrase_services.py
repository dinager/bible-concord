import json
import traceback
from typing import Any, Tuple

from server.db_model.model.phrase import PhraseModel
from server.db_model.model.phrase_reference import PhraseReferenceModel


def add_phrase(phrase_name: str) -> Tuple[bool, str]:
    try:
        phrase_name = phrase_name.lower()
        if PhraseModel.does_phrase_exist(phrase_name):
            return False, f"phrase {phrase_name} already exists"

        references = PhraseReferenceModel.find_references_of_phrase(phrase_name)
        if len(references) == 0:
            return False, f"phrase name {phrase_name} wasn't found in the text"
        PhraseModel.insert_phrase_to_tables(phrase_name, references)
        return True, f"phrase {phrase_name} added successfully"

    except Exception as e:
        print(traceback.format_exc())
        return False, str(e)


def get_phrases() -> Tuple[bool, str]:
    # the return string is a JSON string
    try:
        phrase_names = PhraseModel.get_all_phrases_names()
        return True, json.dumps({"phrases": list(phrase_names)})

    except Exception as e:
        print(traceback.format_exc())
        return False, str(e)


def get_phrase_references(phrase_name: str) -> list[dict[str, Any]]:
    phrase_id = PhraseModel.get_phrase_id(phrase_name)
    references = PhraseReferenceModel.get_all_phrase_references(phrase_id)
    phrase_references = [
        {
            "title": reference.get("book_title"),
            "chapter_num": reference.get("chapter_num"),
            "verse_num": reference.get("verse_num"),
            "word_position": reference.get("word_position"),
        }
        for reference in references
    ]
    return phrase_references
