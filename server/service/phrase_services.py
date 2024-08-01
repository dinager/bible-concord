import json
import traceback
from typing import Any, Tuple

from server.db_model.model.phrase import PhraseModel
from server.db_model.model.word_appearance import WordAppearanceModel


def add_phrase(phrase_text: str) -> Tuple[bool, str]:
    try:
        phrase_text = phrase_text.lower()
        if PhraseModel.does_phrase_exist(phrase_text):
            return False, f"phrase '{phrase_text}' already exists"

        references = WordAppearanceModel.find_all_references_of_phrase(phrase_text)
        if len(references) == 0:
            return False, f"phrase '{phrase_text}' wasn't found in the text"
        PhraseModel.insert_phrase(phrase_text)
        return True, f"phrase {phrase_text} added successfully"

    except Exception as e:
        print(traceback.format_exc())
        return False, str(e)


def get_phrases() -> Tuple[bool, str]:
    # the return string is a JSON string
    try:
        phrases = PhraseModel.get_all_phrases()
        return True, json.dumps({"phrases": list(phrases)})

    except Exception as e:
        print(traceback.format_exc())
        return False, str(e)


def get_phrase_references(phrase_text: str) -> list[dict[str, Any]]:
    references = WordAppearanceModel.find_all_references_of_phrase(phrase_text)

    phrase_references = [
        {
            "title": reference.get("book"),
            "chapter_num": reference.get("chapter"),
            "verse_num": reference.get("verse"),
            "word_position": reference.get("indexInVerse"),
        }
        for reference in references
    ]
    return phrase_references
