import traceback
from typing import Tuple

from server.db_model.model.word_appearance import WordAppearanceModel


def get_num_words_in_verse(book_name: str, chapter_num: int, verse_num: int) -> Tuple[bool, str | int]:
    try:
        book_name = book_name.lower()
        num_words = WordAppearanceModel.get_num_words(book_name, chapter_num, verse_num)
        if num_words == -1:
            return False, f"Book {book_name} was not found"
        if num_words == 0:
            return False, f"no words found in chapter number {chapter_num} verse number {verse_num}"
        return True, num_words

    except Exception as e:
        print(traceback.format_exc())
        return False, str(e)
