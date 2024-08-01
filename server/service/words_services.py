import traceback
from typing import Tuple

from server.db_model.model.book import BookModel
from server.db_model.model.word_appearance import WordAppearanceModel


def get_word_text_context(book_name: str, chapter: int, verse: int) -> Tuple[bool, str]:
    try:
        book_id = BookModel.get_book_id(book_name.lower())
        fetched_context = WordAppearanceModel.construct_context(book_id, chapter, verse)
        return True, fetched_context

    except Exception as e:
        print(traceback.format_exc())
        return False, str(e)
